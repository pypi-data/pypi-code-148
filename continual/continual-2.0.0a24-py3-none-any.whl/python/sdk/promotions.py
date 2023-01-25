from __future__ import annotations
from typing import List, Optional
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.tags import TagsManager
from continual.python.sdk.metadata import MetadataManager


class PromotionManager(Manager):
    """Manages promotion resources."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}/promotions/{promotion}"

    def create(
        self,
        reason: str,
        model_version: str,
        improvement_metric: str,
        improvement_metric_value: float,
        base_improvement_metric_value: float,
        improvement_metric_diff: float,
        base_model_version: Optional[str] = None,
        id: Optional[str] = None,
        state: Optional[str] = "STATE_UNSPECIFIED",
        message: Optional[str] = None,
        update_if_exists: bool = True,
    ) -> Promotion:
        """Create promotion.

        Arguments:
            reason: A description of why the model version is being promoted
            model_version: The name of the model_version
            improvement_metric: The name of the metric that was considered
            improvement_metric_value: The value of the metric that was considered if improved
            base_improvement_metric_value: The value of the metric that was improved upon
            id: Optional Promotion id.
            state: Optional Promotion state e.g. "STATE_UNSPECIFIED", "SUCCEEDED", "FAILED"
            message: Optional Promotion message
            update_if_exists: If True, will update the promotion if it already exists. If False, will throw an error if the promotion already exists.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> model.promotions.create(model_version=model_version.name, reason="UPLIFT")
            <Promotion object {'name': 'projects/test_proj_4/environments/test_env/models/my_model/promotions/ceg9c025lsrt9r5a8l70',
            'create_time': '2022-12-19T16:49:04.118916Z', 'model_version': 'projects/test_proj_4/environments/test_env/models/my_model/versions/ceg99oq5lsrt9r5a8l2g',
            'reason': 'UPLIFT', 'account': 'users/BefwyWcn6x7SNC533zfaAR',
            'run_name': 'projects/test_proj_4/environments/test_env/runs/ceg93ji5lsrt9r5a8kt0', 'base_model_version': '',
            'state': 'STATE_UNSPECIFIED', 'improvement_metric': '', 'improvement_metric_value': 0.0, 'base_improvement_metric_value': 0.0,
            'improvement_metric_diff': 0.0, 'message': ''}>
        """
        req = management_pb2.CreatePromotionRequest(
            parent=self.parent,
            promotion=Promotion(
                reason=reason,
                base_model_version=base_model_version,
                model_version=model_version,
                improvement_metric=improvement_metric,
                improvement_metric_value=improvement_metric_value,
                base_improvement_metric_value=base_improvement_metric_value,
                improvement_metric_diff=improvement_metric_diff,
                state=state,
                message=message,
                run=self.run_name,
            ).to_proto(),
            promotion_id=id,
            update_if_exists=update_if_exists,
        )
        resp = self.client._management.CreatePromotion(req)
        return Promotion.from_proto(resp, client=self.client)

    def get(self, id: str) -> Promotion:
        """Get promotion.

        Arguments:
            id: Promotion name or id.

        Returns
            A promotion.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> promotion = model.promotions.create(model_version_name=model_version.name, reason="UPLIFT")
            >>> model.promotions.get(promotion.id)
            <Promotion object {'name': 'projects/test_proj_4/environments/test_env/models/my_model/promotions/ceg9c025lsrt9r5a8l70',
            'create_time': '2022-12-19T16:49:04.118916Z', 'model_version': 'projects/test_proj_4/environments/test_env/models/my_model/versions/ceg99oq5lsrt9r5a8l2g',
            'reason': 'UPLIFT', 'account': 'users/BefwyWcn6x7SNC533zfaAR',
            'run_name': 'projects/test_proj_4/environments/test_env/runs/ceg93ji5lsrt9r5a8kt0', 'base_model_version': '',
            'state': 'STATE_UNSPECIFIED', 'improvement_metric': '', 'improvement_metric_value': 0.0, 'base_improvement_metric_value': 0.0,
            'improvement_metric_diff': 0.0, 'message': ''}>
        """
        req = management_pb2.GetPromotionRequest(name=self.name(id))
        resp = self.client._management.GetPromotion(req)
        return Promotion.from_proto(resp, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: Optional[str] = None,
        latest: bool = True,
    ) -> List[Promotion]:
        """List promotions.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.

        Returns:
            A list of Promotions.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> promos = [model.promotions.create(reason="UPLIFT", model_version_name=model_version.name) for _ in range(3)]
            >>> len(model.promotions.list(page_size=10))
            3
        """
        req = management_pb2.ListPromotionsRequest(
            parent=self.parent, page_size=page_size, order_by=order_by, latest=latest
        )
        resp = self.client._management.ListPromotions(req)
        return [Promotion.from_proto(x, client=self.client) for x in resp.promotions]

    def list_all(self) -> Pager[Promotion]:
        """List all promotions.

        Pages through all promotions using an iterator.

        Returns:
            A iterator of all promotions.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> promos = [model.promotions.create(reason="UPLIFT", model_version_name=model_version.name) for _ in range(3)]
            >>> len(model.promotions.list_all())
            3
        """

        def next_page(next_page_token):
            req = management_pb2.ListPromotionsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListPromotions(req)
            return (
                [Promotion.from_proto(x, client=self.client) for x in resp.promotions],
                resp.next_page_token,
            )

        return Pager(next_page)


class Promotion(Resource, types.Promotion):
    """Promotion resource."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}/promotions/{promotion}"
    _manager: PromotionManager
    """Promotion Manager."""

    _metadata: MetadataManager
    """Metadata Manager"""

    _tags: TagsManager
    """Tags Manager"""

    def _init(self):
        self._manager = PromotionManager(parent=self.parent, client=self.client)
        self._metadata = MetadataManager(parent=self.name, client=self.client)
        self._tags = TagsManager(parent=self.name, client=self.client)

    @property
    def metadata(self) -> MetadataManager:
        """Metadata Manager"""
        return self._metadata

    @property
    def tags(self) -> TagsManager:
        """Tags Manager"""
        return self._tags
