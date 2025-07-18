from odoo.exceptions import UserError, ValidationError
import requests
from odoo import api, fields, models, _
from markupsafe import Markup
import logging

_logger = logging.getLogger(__name__)


class CommunicationChannel(models.Model):
    _inherit = 'discuss.channel'

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        rdata = super(CommunicationChannel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
        chatgpt_channel_id = self.env.ref('odoo_turbo_ai_agent.channel_chatgpt')
        user_chatgpt = self.env.ref("odoo_turbo_ai_agent.user_chatgpt")
        partner_chatgpt = self.env.ref("odoo_turbo_ai_agent.partner_chatgpt")
        author_id = msg_vals.get('author_id')
        chatgpt_name = str(partner_chatgpt.name or '') + ', '
        prompt = msg_vals.get('body')

        if not prompt:
            return rdata
        try:
            if author_id != partner_chatgpt.id and (chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', '')) and self.channel_type == 'chat':
                res = self._get_chatgpt_response(prompt=prompt)
                self.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
            elif author_id != partner_chatgpt.id and msg_vals.get('model', '') == 'discuss.channel' and msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
                res = self._get_chatgpt_response(prompt=prompt)
                chatgpt_channel_id.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')

        except Exception as e:
            # Log or handle exceptions more specifically
            _logger.error("Error in ChatGPT response: %s", e)
            pass

        return rdata

    def _get_chatgpt_response(self, prompt):
        ICP = self.env['ir.config_parameter'].sudo()
        ai_provider = ICP.get_param('odoo_turbo_ai_agent.ai_provider', 'openai')
        
        if ai_provider == 'mistral':
            return self._get_mistral_response(prompt)
        else:
            return self._get_openai_response(prompt)
    
    def _get_openai_response(self, prompt):
        # Replace with the actual ChatGPT endpoint URL
        ICP = self.env['ir.config_parameter'].sudo()
        api_key = ICP.get_param('odoo_turbo_ai_agent.openapi_api_key')

        gpt_model_id = ICP.get_param('odoo_turbo_ai_agent.chatgpt_model_id')

        domain = ICP.get_param('web.base.url')
        db_name = ICP.get_param('odoo_turbo_ai_agent.odoodb_dbname')
        db_user = ICP.get_param('odoo_turbo_ai_agent.odoodb_user')
        db_password = ICP.get_param('odoo_turbo_ai_agent.odoodb_password')
        db_host = ICP.get_param('odoo_turbo_ai_agent.odoodb_host')
        db_port = ICP.get_param('odoo_turbo_ai_agent.odoodb_port')
        # Get the Odoo user and password
        odoo_user = ICP.get_param('odoo_turbo_ai_agent.odoo_user')
        odoo_password = ICP.get_param('odoo_turbo_ai_agent.odoo_password')

        gpt_model = 'gpt-3.5-turbo'
        try:
            if gpt_model_id:
                gpt_model = self.env['chatgpt.model'].browse(int(gpt_model_id)).name
        except Exception as ex:
            gpt_model = 'gpt-3.5-turbo'
            _logger.error("Error in ChatGPT response: %s", ex)
            pass

        # Make the API request
        turboclient_url = "https://turboaiagent.techspawn.net/chat_response"
        messages_for = str(prompt)
        turboclient_body = {
            "message": messages_for,
            "api_key": api_key,
            "modal_name": gpt_model,
            "domain": domain,
            "db_name": db_name,
            "db_user": db_user,
            "db_password": db_password,
            "db_host": db_host,
            "db_port": db_port,
            "odoo_user": odoo_user,
            "odoo_password": odoo_password,
            }
        headers = {
            "Content-Type": "text/plain",
        }
        try:
            turboclient_response = requests.post(turboclient_url, headers=headers, json=turboclient_body)
            turboclient_response.raise_for_status()
            # Parse the response (assuming JSON format based on OpenAI API)
            turboclient_data = turboclient_response.json()
            turboclient_data_res = turboclient_data.get('message')
            return Markup(turboclient_data_res)
        except requests.exceptions.RequestException as e:
            _logger.error("Error in OpenAI response: %s", e)
            return "Something is wrong with OpenAI!! ☹️."
        except Exception as e:
            _logger.error("Error in OpenAI response: %s", e)
            return str(e)
    
    def _get_mistral_response(self, prompt):
        ICP = self.env['ir.config_parameter'].sudo()
        api_key = ICP.get_param('odoo_turbo_ai_agent.mistral_api_key')
        
        if not api_key:
            return "❌ Mistral API Key no configurada. Ve a Configuración → Ajustes → Turbo AIAgent 🚀"
        
        model_id = ICP.get_param('odoo_turbo_ai_agent.chatgpt_model_id')
        model_name = 'mistral-7b-instruct'
        
        try:
            if model_id:
                model_name = self.env['chatgpt.model'].browse(int(model_id)).name
        except Exception as ex:
            model_name = 'mistral-7b-instruct'
            _logger.error("Error getting Mistral model: %s", ex)
        
        # Mistral API endpoint
        mistral_url = "https://api.mistral.ai/v1/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": str(prompt)
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(mistral_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            response_data = response.json()
            if 'choices' in response_data and len(response_data['choices']) > 0:
                message_content = response_data['choices'][0]['message']['content']
                return Markup(f"🤖 **Mistral AI ({model_name}):**\n\n{message_content}")
            else:
                return "❌ No se recibió respuesta válida de Mistral AI"
                
        except requests.exceptions.RequestException as e:
            _logger.error("Error in Mistral API request: %s", e)
            return f"❌ Error de conexión con Mistral AI: {str(e)}"
        except Exception as e:
            _logger.error("Error in Mistral response: %s", e)
            return f"❌ Error procesando respuesta de Mistral: {str(e)}"
