from django.utils.encoding import force_str
from rest_framework import status
from rest_framework.renderers import JSONRenderer


class CustomResponseRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context.get("response").status_code

        if status_code < status.HTTP_400_BAD_REQUEST:  # GOOD RESPONSE
            response_data = self.good_response(data, status_code)

        else:  # BAD RESPONSE
            response_data = self.bad_response(data, status_code)

        return super(CustomResponseRenderer, self).render(
            response_data, accepted_media_type, renderer_context
        )

    @staticmethod
    def good_response(data, status_code):
        return {
            "status": status_code,
            "message": data.pop("message", None),
            "data": data.pop("data"),
            "errors": None,
        }

    @staticmethod
    def bad_response(data, status_code):
        general_message, errors = CustomResponseRenderer._extract_errors(
            data, status_code
        )
        message = (
            general_message
            or data.pop("message", None)
            or (
                force_str(
                    data.pop(
                        "detail",
                        "An error occurred, please check your data and try again.",
                    )
                )
                if status_code >= status.HTTP_400_BAD_REQUEST
                else "Request submitted successfully"
            )
        )

        data.pop("non_field_errors", None)  # Remove unnecessary keys

        return {
            "status": status_code,
            "message": message,
            "data": None,
            "errors": errors or None,
        }

    @staticmethod
    def _extract_errors(data, status_code):
        """Extracts validation and authentication errors in a consistent format."""
        if not isinstance(data, dict):
            return None, None

        # Handle token authentication errors
        if (
            data.get("code") == "token_not_valid"
            and status_code == status.HTTP_401_UNAUTHORIZED
        ):
            return (
                data.get("messages", [{"message": "Token is invalid or expired"}])[
                    0
                ].get("message"),
                None,
            )

        errors = []

        general_message = data.get("non_field_errors", [None])[0]

        for field, messages in data.items():
            if isinstance(messages, list) and len(messages) > 1:
                for msg in messages:
                    errors.append({"field": field, "message": str(msg)})

            elif isinstance(messages, list) and len(messages) == 1:
                general_message = f"{messages[0]}"
                errors.append({"field": field, "message": str(messages[0])})

            elif isinstance(messages, dict):

                for k, v in messages.items():
                    __message = []
                    if isinstance(v, list):
                        if len(v) == 1:
                            __message = str(v[0]).replace('"', "")
                        else:
                            __message = [str(m).replace('"', "") for m in v]

                    elif isinstance(v, dict):
                        for d_v in v.values():
                            __message.append(str(d_v[0]).replace('"', ""))

                    errors.append({"field": k, "message": __message})

        return general_message, errors
