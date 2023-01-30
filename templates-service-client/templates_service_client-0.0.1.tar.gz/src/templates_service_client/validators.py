from pydantic import BaseModel


class OperatorOnboardingValidator(BaseModel):
    project: str
    organization_name: str
    app_path: str
    web_path: str

    def get_dict(self) -> dict:
        return {k: str(v) for k, v in self.__dict__.items()}


class GenericStrResponse(BaseModel):

    response: str

    def get_dict(self) -> dict:
        return {k: str(v) for k, v in self.__dict__.items()}


class GenericDictResponse(BaseModel):

    response: dict

    def get_dict(self) -> dict:
        return {k: str(v) for k, v in self.__dict__.items()}