from typing import Optional
from django.http import HttpRequest
from rest_framework.views import APIView

from rudra.paginator import PaginatorService
from rudra.service import get_model, get_models, get_serializer, get_success_response, get_error_response, check_method_allowed, get_serializer_context, get_user_serializer
from rest_framework.serializers import Serializer


class AllModels(APIView):
    def get(self, request: HttpRequest):

        models = get_models()

        models_with_fields = {}

        for model in models:
            models_with_fields[model.__name__] = [{
                'name': field.name,
                'type': field.get_internal_type(),
                'related_model': field.related_model.__name__ if field.related_model else None,
                'description': field.description if hasattr(field, 'description') else None
            } for field in model._meta.get_fields()]

        return get_success_response(models_with_fields)

class User(APIView):
    def get(self, request: HttpRequest):
        user_serializer = get_user_serializer()
        if user_serializer:
            if not request.user.is_authenticated:
                return get_error_response('User not authenticated')
            return get_success_response(user_serializer(request.user).data)
        return get_error_response('User serializer not found')

class QueryModel(APIView):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        method = request.method.lower()
        model_name = kwargs.get('model_name')
        model = get_model(model_name)

        if not model:
            return get_error_response('Model not found')

        if not check_method_allowed(model, method):
            return get_error_response('Method not allowed')
        
        self.model = model        
        self.serializer = get_serializer(model, method=method)
        self.serializer_context = get_serializer_context(request)

        return super().dispatch(request, *args, **kwargs)
    
    def is_valid_data(self, serializer: Serializer) -> Optional[str]:
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return str(e)

    def get(self, request: HttpRequest, model_name: str):
        filters = request.GET.dict()
        all = bool(filters.pop('all', False))
        page = filters.pop('page', None)
        page_size = filters.pop('page_size', None)
        order_by = filters.pop('order_by', None)
        instance = self.model.objects.filter(**filters)

        if all:
            instance = instance.all()
            return get_success_response(self.serializer(instance, many=True, context=self.serializer_context).data)
        elif page:
            if not order_by:
                order_by = '-id'
            instance = instance.order_by(order_by)
            paginator = PaginatorService(instance, page=page or 1, page_size=page_size or 10)
            return get_success_response(self.serializer(paginator.get_query_set(), many=True, context=self.serializer_context).data, paginator)
        else:
            instance = instance.first()
            if not instance:
                return get_error_response('Not found')
            return get_success_response(self.serializer(instance, context=self.serializer_context).data)

    def post(self, request: HttpRequest, model_name: str):
        data = request.data
        serializer = self.serializer(data=data, context=self.serializer_context)
        error = self.is_valid_data(serializer)
        if error:
            return get_error_response(error)
        instance = serializer.save()
        return get_success_response(self.serializer(instance, context=self.serializer_context).data)
    
    def put(self, request: HttpRequest, model_name: str):
        data = request.data
        serializer = self.serializer(data=data, context=self.serializer_context)
        error = self.is_valid_data(serializer)
        if error:
            return get_error_response(error)
        instance = serializer.save()
        return get_success_response(self.serializer(instance, context=self.serializer_context).data)
    
    def patch(self, request: HttpRequest, model_name: str):
        data = request.data
        serializer = self.serializer(data=data, context=self.serializer_context)
        error = self.is_valid_data(serializer)
        if error:
            return get_error_response(error)
        instance = serializer.save()
        return get_success_response(self.serializer(instance, context=self.serializer_context).data)
    
    def delete(self, request: HttpRequest, model_name: str):
        data = request.data
        instance = self.model.objects.filter(**data).first()
        if not instance:
            return get_error_response('Instance not found')
        instance.delete()
        return get_success_response()

class DeepQueryModel(APIView):

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        method = request.method.lower()
        model_name = kwargs.get('model_name')
        model = get_model(model_name)

        if not model:
            return get_error_response('Model not found')

        if not check_method_allowed(model, method):
            return get_error_response('Method not allowed')
        
        self.model = model        
        self.serializer = get_serializer(model, method=method)
        self.serializer_context = get_serializer_context(request)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, model_name: str):
        data = request.data
        query_params = request.GET.dict()
        model = get_model(model_name)
        if not model:
            return get_error_response('Model not found')

        object_manager = model.objects

        # Select related query
        select_related = data.get('select_related', [])
        if select_related:
            object_manager = object_manager.select_related(*select_related)

        # Prefetch related query 
        prefetch_related = data.get('prefetch_related', [])
        if prefetch_related:
            object_manager = object_manager.prefetch_related(*prefetch_related)
        
        filters = data.get('filters', {})
        instance = object_manager.filter(**filters)

        order_by_list = data.get('order_by_list', [])

        if order_by_list:
            instance = instance.order_by(*order_by_list)
        
        all = bool(query_params.get('all', False))
        page = query_params.get('page', None)
        page_size = query_params.get('page_size', None)

        if all:
            instance = instance.all()
            return get_success_response(self.serializer(instance, many=True, context=self.serializer_context).data)
        elif page:
            if not order_by_list:
                order_by_list = ['-id']
            instance = instance.order_by(*order_by_list)
            paginator = PaginatorService(instance, page=page or 1, page_size=page_size or 10)
            return get_success_response(self.serializer(paginator.get_query_set(), many=True, context=self.serializer_context).data, paginator)
        else:
            instance = instance.first()
            if not instance:
                return get_error_response('Instance not found')
            return get_success_response(self.serializer(instance, context=self.serializer_context).data)