from enum import Enum, unique
from flask import jsonify
class ResponseType(Enum):
    SUCCESS = ('success', 'ok')
    FAILURE = ('failure', '')
    PARAMETERS_ERR = ('failure', 'parameters error')
    INTERNAL_ERR = ('failure', 'internal error')
    VALIDATION_ERR = ('failure', 'validation error')

class Response():
    def __init__(self, res_type: ResponseType):
        self.response = {
            'status': res_type.value[0],
            'message': res_type.value[1]
        }
    
    def update_attr(self, attr: str, val: object):
        self.response[attr] = val

    def get_response_dict(self):
        return self.response

    def get_json(self):
        return jsonify(self.response)
    
    # @classmethod
    # def get_default_response(cls, res_type: ResponseType):
    #     return cls(res_type[0], res_type[1])
    
    @classmethod
    def get_custom_response(cls, res_type: ResponseType, message: str):
        response = cls(res_type)
        response.update_attr('message', message)
        return response
