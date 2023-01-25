import typing_extensions

from openapi_client.paths import PathValues
from openapi_client.apis.paths.auth_keylogin import AuthKeylogin
from openapi_client.apis.paths.auth_login import AuthLogin
from openapi_client.apis.paths.auth_keygen import AuthKeygen
from openapi_client.apis.paths.auth_who_am_i import AuthWhoAmI
from openapi_client.apis.paths.auth_signup import AuthSignup
from openapi_client.apis.paths.auth_activate import AuthActivate
from openapi_client.apis.paths.auth_resend_activation_mail import AuthResendActivationMail
from openapi_client.apis.paths.auth_send_reset_password_mail import AuthSendResetPasswordMail
from openapi_client.apis.paths.auth_reset_password import AuthResetPassword
from openapi_client.apis.paths.auth_set_user_metadata import AuthSetUserMetadata
from openapi_client.apis.paths.auth_request_trial import AuthRequestTrial
from openapi_client.apis.paths.auth_start_trial import AuthStartTrial
from openapi_client.apis.paths.auth_extend_trial import AuthExtendTrial
from openapi_client.apis.paths.auth_logout import AuthLogout
from openapi_client.apis.paths.dashboards_get_kibana_dashboards import DashboardsGetKibanaDashboards
from openapi_client.apis.paths.dashboards_get_project_dashboards import DashboardsGetProjectDashboards
from openapi_client.apis.paths.dashboards_get_dashboard import DashboardsGetDashboard
from openapi_client.apis.paths.dashboards_add_dashboard import DashboardsAddDashboard
from openapi_client.apis.paths.dashboards_delete_dashboard import DashboardsDeleteDashboard
from openapi_client.apis.paths.dashboards_update_dashboard import DashboardsUpdateDashboard
from openapi_client.apis.paths.dashboards_get_kibana_dashlet_fields import DashboardsGetKibanaDashletFields
from openapi_client.apis.paths.dashboards_get_dashlet_fields import DashboardsGetDashletFields
from openapi_client.apis.paths.datasets_get_datasets import DatasetsGetDatasets
from openapi_client.apis.paths.datasets_add_dataset import DatasetsAddDataset
from openapi_client.apis.paths.datasets_trash_dataset import DatasetsTrashDataset
from openapi_client.apis.paths.datasets_save_dataset_version import DatasetsSaveDatasetVersion
from openapi_client.apis.paths.datasets_modify_dataset_version_note import DatasetsModifyDatasetVersionNote
from openapi_client.apis.paths.datasets_parse_dataset import DatasetsParseDataset
from openapi_client.apis.paths.datasets_get_dataset_version import DatasetsGetDatasetVersion
from openapi_client.apis.paths.datasets_get_latest_dataset_version import DatasetsGetLatestDatasetVersion
from openapi_client.apis.paths.datasets_get_dataset_versions import DatasetsGetDatasetVersions
from openapi_client.apis.paths.demos_get_demos import DemosGetDemos
from openapi_client.apis.paths.demos_import_demo_project import DemosImportDemoProject
from openapi_client.apis.paths.demos_send_user_message import DemosSendUserMessage
from openapi_client.apis.paths.exportedmodels_get_exported_model_jobs import ExportedmodelsGetExportedModelJobs
from openapi_client.apis.paths.exportedmodels_get_stored_exported_model_resource_url import ExportedmodelsGetStoredExportedModelResourceUrl
from openapi_client.apis.paths.insights_get_model_insights import InsightsGetModelInsights
from openapi_client.apis.paths.issues_get_project_issues import IssuesGetProjectIssues
from openapi_client.apis.paths.issues_get_single_issue import IssuesGetSingleIssue
from openapi_client.apis.paths.issues_update_issue import IssuesUpdateIssue
from openapi_client.apis.paths.issues_add_issue import IssuesAddIssue
from openapi_client.apis.paths.issues_delete_issue import IssuesDeleteIssue
from openapi_client.apis.paths.jobs_get_jobs import JobsGetJobs
from openapi_client.apis.paths.jobs_get_training_jobs import JobsGetTrainingJobs
from openapi_client.apis.paths.jobs_is_training_job_running import JobsIsTrainingJobRunning
from openapi_client.apis.paths.jobs_get_organization_jobs import JobsGetOrganizationJobs
from openapi_client.apis.paths.jobs_stop_job import JobsStopJob
from openapi_client.apis.paths.jobs_terminate_job import JobsTerminateJob
from openapi_client.apis.paths.jobs_warmup import JobsWarmup
from openapi_client.apis.paths.jobs_add_export_model_job import JobsAddExportModelJob
from openapi_client.apis.paths.jobs_train_from_scratch import JobsTrainFromScratch
from openapi_client.apis.paths.jobs_continue_train import JobsContinueTrain
from openapi_client.apis.paths.jobs_train_from_initial_weights import JobsTrainFromInitialWeights
from openapi_client.apis.paths.jobs_evaluate import JobsEvaluate
from openapi_client.apis.paths.jobs_sample_analysis import JobsSampleAnalysis
from openapi_client.apis.paths.jobs_population_exploration import JobsPopulationExploration
from openapi_client.apis.paths.jobs_sample_selection import JobsSampleSelection
from openapi_client.apis.paths.jobs_get_machine_types import JobsGetMachineTypes
from openapi_client.apis.paths.jobs_set_machine_type import JobsSetMachineType
from openapi_client.apis.paths.metadata_get_max_active_users import MetadataGetMaxActiveUsers
from openapi_client.apis.paths.metadata_get_statistics import MetadataGetStatistics
from openapi_client.apis.paths.model_tests_create_model_test import ModelTestsCreateModelTest
from openapi_client.apis.paths.model_tests_update_model_test import ModelTestsUpdateModelTest
from openapi_client.apis.paths.model_tests_get_single_model_test import ModelTestsGetSingleModelTest
from openapi_client.apis.paths.model_tests_get_all_project_model_tests import ModelTestsGetAllProjectModelTests
from openapi_client.apis.paths.model_tests_delete_model_test import ModelTestsDeleteModelTest
from openapi_client.apis.paths.model_tests_get_model_test_result import ModelTestsGetModelTestResult
from openapi_client.apis.paths.modelmetrics_get_model_epoch_loss import ModelmetricsGetModelEpochLoss
from openapi_client.apis.paths.modelmetrics_get_xy_chart import ModelmetricsGetXYChart
from openapi_client.apis.paths.modelmetrics_get_heatmap_chart import ModelmetricsGetHeatmapChart
from openapi_client.apis.paths.modelmetrics_get_table_chart import ModelmetricsGetTableChart
from openapi_client.apis.paths.modelmetrics_get_confusion_metric_names import ModelmetricsGetConfusionMetricNames
from openapi_client.apis.paths.modelmetrics_get_balanced_accuracy import ModelmetricsGetBalancedAccuracy
from openapi_client.apis.paths.modelmetrics_get_f1_score import ModelmetricsGetF1Score
from openapi_client.apis.paths.modelmetrics_get_pr_curve import ModelmetricsGetPrCurve
from openapi_client.apis.paths.modelmetrics_get_roc import ModelmetricsGetRoc
from openapi_client.apis.paths.models_get_models_by_hash import ModelsGetModelsByHash
from openapi_client.apis.paths.models_get_models_by_version_id import ModelsGetModelsByVersionId
from openapi_client.apis.paths.models_get_recent_organization_models import ModelsGetRecentOrganizationModels
from openapi_client.apis.paths.models_delete_model import ModelsDeleteModel
from openapi_client.apis.paths.monitor_health_check import MonitorHealthCheck
from openapi_client.apis.paths.notifications_get_notifications import NotificationsGetNotifications
from openapi_client.apis.paths.notifications_set_user_notifications_as_read import NotificationsSetUserNotificationsAsRead
from openapi_client.apis.paths.organizations_get_organizations import OrganizationsGetOrganizations
from openapi_client.apis.paths.organizations_update_organization_public_name import OrganizationsUpdateOrganizationPublicName
from openapi_client.apis.paths.organizations_create_organization import OrganizationsCreateOrganization
from openapi_client.apis.paths.organizations_delete_organization import OrganizationsDeleteOrganization
from openapi_client.apis.paths.organizations_set_default_organization import OrganizationsSetDefaultOrganization
from openapi_client.apis.paths.projects_add_project import ProjectsAddProject
from openapi_client.apis.paths.projects_get_projects import ProjectsGetProjects
from openapi_client.apis.paths.projects_load_model import ProjectsLoadModel
from openapi_client.apis.paths.projects_delete_project import ProjectsDeleteProject
from openapi_client.apis.paths.projects_trash_project import ProjectsTrashProject
from openapi_client.apis.paths.projects_get_current_project_version import ProjectsGetCurrentProjectVersion
from openapi_client.apis.paths.secret_manager_add_secret_manager import SecretManagerAddSecretManager
from openapi_client.apis.paths.secret_manager_trash_secret_manager import SecretManagerTrashSecretManager
from openapi_client.apis.paths.secret_manager_get_secret_manager_list import SecretManagerGetSecretManagerList
from openapi_client.apis.paths.secret_manager_update_secret_manager import SecretManagerUpdateSecretManager
from openapi_client.apis.paths.users_get_organization_slim_user_data import UsersGetOrganizationSlimUserData
from openapi_client.apis.paths.users_get_all_slim_user_data import UsersGetAllSlimUserData
from openapi_client.apis.paths.users_update_user_status import UsersUpdateUserStatus
from openapi_client.apis.paths.users_update_user_organization import UsersUpdateUserOrganization
from openapi_client.apis.paths.users_update_user_role import UsersUpdateUserRole
from openapi_client.apis.paths.users_update_user_name import UsersUpdateUserName
from openapi_client.apis.paths.users_delete_user_by_id import UsersDeleteUserById
from openapi_client.apis.paths.versions_import_model import VersionsImportModel
from openapi_client.apis.paths.versions_add_version import VersionsAddVersion
from openapi_client.apis.paths.versions_load_version import VersionsLoadVersion
from openapi_client.apis.paths.versions_delete_version import VersionsDeleteVersion
from openapi_client.apis.paths.versions_update_version import VersionsUpdateVersion
from openapi_client.apis.paths.versions_get_project_slim_versions import VersionsGetProjectSlimVersions
from openapi_client.apis.paths.versions_get_upload_signed_url import VersionsGetUploadSignedUrl
from openapi_client.apis.paths.visualizations_get_visualization import VisualizationsGetVisualization
from openapi_client.apis.paths.visualizations_get_model_visualizations import VisualizationsGetModelVisualizations
from openapi_client.apis.paths.visualizations_save_analyzer_layout import VisualizationsSaveAnalyzerLayout
from openapi_client.apis.paths.visualizations_delete_visualizations import VisualizationsDeleteVisualizations
from openapi_client.apis.paths.visualizations_get_stored_resource_url import VisualizationsGetStoredResourceUrl

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.AUTH_KEYLOGIN: AuthKeylogin,
        PathValues.AUTH_LOGIN: AuthLogin,
        PathValues.AUTH_KEYGEN: AuthKeygen,
        PathValues.AUTH_WHO_AM_I: AuthWhoAmI,
        PathValues.AUTH_SIGNUP: AuthSignup,
        PathValues.AUTH_ACTIVATE: AuthActivate,
        PathValues.AUTH_RESEND_ACTIVATION_MAIL: AuthResendActivationMail,
        PathValues.AUTH_SEND_RESET_PASSWORD_MAIL: AuthSendResetPasswordMail,
        PathValues.AUTH_RESET_PASSWORD: AuthResetPassword,
        PathValues.AUTH_SET_USER_METADATA: AuthSetUserMetadata,
        PathValues.AUTH_REQUEST_TRIAL: AuthRequestTrial,
        PathValues.AUTH_START_TRIAL: AuthStartTrial,
        PathValues.AUTH_EXTEND_TRIAL: AuthExtendTrial,
        PathValues.AUTH_LOGOUT: AuthLogout,
        PathValues.DASHBOARDS_GET_KIBANA_DASHBOARDS: DashboardsGetKibanaDashboards,
        PathValues.DASHBOARDS_GET_PROJECT_DASHBOARDS: DashboardsGetProjectDashboards,
        PathValues.DASHBOARDS_GET_DASHBOARD: DashboardsGetDashboard,
        PathValues.DASHBOARDS_ADD_DASHBOARD: DashboardsAddDashboard,
        PathValues.DASHBOARDS_DELETE_DASHBOARD: DashboardsDeleteDashboard,
        PathValues.DASHBOARDS_UPDATE_DASHBOARD: DashboardsUpdateDashboard,
        PathValues.DASHBOARDS_GET_KIBANA_DASHLET_FIELDS: DashboardsGetKibanaDashletFields,
        PathValues.DASHBOARDS_GET_DASHLET_FIELDS: DashboardsGetDashletFields,
        PathValues.DATASETS_GET_DATASETS: DatasetsGetDatasets,
        PathValues.DATASETS_ADD_DATASET: DatasetsAddDataset,
        PathValues.DATASETS_TRASH_DATASET: DatasetsTrashDataset,
        PathValues.DATASETS_SAVE_DATASET_VERSION: DatasetsSaveDatasetVersion,
        PathValues.DATASETS_MODIFY_DATASET_VERSION_NOTE: DatasetsModifyDatasetVersionNote,
        PathValues.DATASETS_PARSE_DATASET: DatasetsParseDataset,
        PathValues.DATASETS_GET_DATASET_VERSION: DatasetsGetDatasetVersion,
        PathValues.DATASETS_GET_LATEST_DATASET_VERSION: DatasetsGetLatestDatasetVersion,
        PathValues.DATASETS_GET_DATASET_VERSIONS: DatasetsGetDatasetVersions,
        PathValues.DEMOS_GET_DEMOS: DemosGetDemos,
        PathValues.DEMOS_IMPORT_DEMO_PROJECT: DemosImportDemoProject,
        PathValues.DEMOS_SEND_USER_MESSAGE: DemosSendUserMessage,
        PathValues.EXPORTEDMODELS_GET_EXPORTED_MODEL_JOBS: ExportedmodelsGetExportedModelJobs,
        PathValues.EXPORTEDMODELS_GET_STORED_EXPORTED_MODEL_RESOURCE_URL: ExportedmodelsGetStoredExportedModelResourceUrl,
        PathValues.INSIGHTS_GET_MODEL_INSIGHTS: InsightsGetModelInsights,
        PathValues.ISSUES_GET_PROJECT_ISSUES: IssuesGetProjectIssues,
        PathValues.ISSUES_GET_SINGLE_ISSUE: IssuesGetSingleIssue,
        PathValues.ISSUES_UPDATE_ISSUE: IssuesUpdateIssue,
        PathValues.ISSUES_ADD_ISSUE: IssuesAddIssue,
        PathValues.ISSUES_DELETE_ISSUE: IssuesDeleteIssue,
        PathValues.JOBS_GET_JOBS: JobsGetJobs,
        PathValues.JOBS_GET_TRAINING_JOBS: JobsGetTrainingJobs,
        PathValues.JOBS_IS_TRAINING_JOB_RUNNING: JobsIsTrainingJobRunning,
        PathValues.JOBS_GET_ORGANIZATION_JOBS: JobsGetOrganizationJobs,
        PathValues.JOBS_STOP_JOB: JobsStopJob,
        PathValues.JOBS_TERMINATE_JOB: JobsTerminateJob,
        PathValues.JOBS_WARMUP: JobsWarmup,
        PathValues.JOBS_ADD_EXPORT_MODEL_JOB: JobsAddExportModelJob,
        PathValues.JOBS_TRAIN_FROM_SCRATCH: JobsTrainFromScratch,
        PathValues.JOBS_CONTINUE_TRAIN: JobsContinueTrain,
        PathValues.JOBS_TRAIN_FROM_INITIAL_WEIGHTS: JobsTrainFromInitialWeights,
        PathValues.JOBS_EVALUATE: JobsEvaluate,
        PathValues.JOBS_SAMPLE_ANALYSIS: JobsSampleAnalysis,
        PathValues.JOBS_POPULATION_EXPLORATION: JobsPopulationExploration,
        PathValues.JOBS_SAMPLE_SELECTION: JobsSampleSelection,
        PathValues.JOBS_GET_MACHINE_TYPES: JobsGetMachineTypes,
        PathValues.JOBS_SET_MACHINE_TYPE: JobsSetMachineType,
        PathValues.METADATA_GET_MAX_ACTIVE_USERS: MetadataGetMaxActiveUsers,
        PathValues.METADATA_GET_STATISTICS: MetadataGetStatistics,
        PathValues.MODELTESTS_CREATE_MODEL_TEST: ModelTestsCreateModelTest,
        PathValues.MODELTESTS_UPDATE_MODEL_TEST: ModelTestsUpdateModelTest,
        PathValues.MODELTESTS_GET_SINGLE_MODEL_TEST: ModelTestsGetSingleModelTest,
        PathValues.MODELTESTS_GET_ALL_PROJECT_MODEL_TESTS: ModelTestsGetAllProjectModelTests,
        PathValues.MODELTESTS_DELETE_MODEL_TEST: ModelTestsDeleteModelTest,
        PathValues.MODELTESTS_GET_MODEL_TEST_RESULT: ModelTestsGetModelTestResult,
        PathValues.MODELMETRICS_GET_MODEL_EPOCH_LOSS: ModelmetricsGetModelEpochLoss,
        PathValues.MODELMETRICS_GET_XYCHART: ModelmetricsGetXYChart,
        PathValues.MODELMETRICS_GET_HEATMAP_CHART: ModelmetricsGetHeatmapChart,
        PathValues.MODELMETRICS_GET_TABLE_CHART: ModelmetricsGetTableChart,
        PathValues.MODELMETRICS_GET_CONFUSION_METRIC_NAMES: ModelmetricsGetConfusionMetricNames,
        PathValues.MODELMETRICS_GET_BALANCED_ACCURACY: ModelmetricsGetBalancedAccuracy,
        PathValues.MODELMETRICS_GET_F1SCORE: ModelmetricsGetF1Score,
        PathValues.MODELMETRICS_GET_PR_CURVE: ModelmetricsGetPrCurve,
        PathValues.MODELMETRICS_GET_ROC: ModelmetricsGetRoc,
        PathValues.MODELS_GET_MODELS_BY_HASH: ModelsGetModelsByHash,
        PathValues.MODELS_GET_MODELS_BY_VERSION_ID: ModelsGetModelsByVersionId,
        PathValues.MODELS_GET_RECENT_ORGANIZATION_MODELS: ModelsGetRecentOrganizationModels,
        PathValues.MODELS_DELETE_MODEL: ModelsDeleteModel,
        PathValues.MONITOR_HEALTH_CHECK: MonitorHealthCheck,
        PathValues.NOTIFICATIONS_GET_NOTIFICATIONS: NotificationsGetNotifications,
        PathValues.NOTIFICATIONS_SET_USER_NOTIFICATIONS_AS_READ: NotificationsSetUserNotificationsAsRead,
        PathValues.ORGANIZATIONS_GET_ORGANIZATIONS: OrganizationsGetOrganizations,
        PathValues.ORGANIZATIONS_UPDATE_ORGANIZATION_PUBLIC_NAME: OrganizationsUpdateOrganizationPublicName,
        PathValues.ORGANIZATIONS_CREATE_ORGANIZATION: OrganizationsCreateOrganization,
        PathValues.ORGANIZATIONS_DELETE_ORGANIZATION: OrganizationsDeleteOrganization,
        PathValues.ORGANIZATIONS_SET_DEFAULT_ORGANIZATION: OrganizationsSetDefaultOrganization,
        PathValues.PROJECTS_ADD_PROJECT: ProjectsAddProject,
        PathValues.PROJECTS_GET_PROJECTS: ProjectsGetProjects,
        PathValues.PROJECTS_LOAD_MODEL: ProjectsLoadModel,
        PathValues.PROJECTS_DELETE_PROJECT: ProjectsDeleteProject,
        PathValues.PROJECTS_TRASH_PROJECT: ProjectsTrashProject,
        PathValues.PROJECTS_GET_CURRENT_PROJECT_VERSION: ProjectsGetCurrentProjectVersion,
        PathValues.SECRETMANAGER_ADD_SECRET_MANAGER: SecretManagerAddSecretManager,
        PathValues.SECRETMANAGER_TRASH_SECRET_MANAGER: SecretManagerTrashSecretManager,
        PathValues.SECRETMANAGER_GET_SECRET_MANAGER_LIST: SecretManagerGetSecretManagerList,
        PathValues.SECRETMANAGER_UPDATE_SECRET_MANAGER: SecretManagerUpdateSecretManager,
        PathValues.USERS_GET_ORGANIZATION_SLIM_USER_DATA: UsersGetOrganizationSlimUserData,
        PathValues.USERS_GET_ALL_SLIM_USER_DATA: UsersGetAllSlimUserData,
        PathValues.USERS_UPDATE_USER_STATUS: UsersUpdateUserStatus,
        PathValues.USERS_UPDATE_USER_ORGANIZATION: UsersUpdateUserOrganization,
        PathValues.USERS_UPDATE_USER_ROLE: UsersUpdateUserRole,
        PathValues.USERS_UPDATE_USER_NAME: UsersUpdateUserName,
        PathValues.USERS_DELETE_USER_BY_ID: UsersDeleteUserById,
        PathValues.VERSIONS_IMPORT_MODEL: VersionsImportModel,
        PathValues.VERSIONS_ADD_VERSION: VersionsAddVersion,
        PathValues.VERSIONS_LOAD_VERSION: VersionsLoadVersion,
        PathValues.VERSIONS_DELETE_VERSION: VersionsDeleteVersion,
        PathValues.VERSIONS_UPDATE_VERSION: VersionsUpdateVersion,
        PathValues.VERSIONS_GET_PROJECT_SLIM_VERSIONS: VersionsGetProjectSlimVersions,
        PathValues.VERSIONS_GET_UPLOAD_SIGNED_URL: VersionsGetUploadSignedUrl,
        PathValues.VISUALIZATIONS_GET_VISUALIZATION: VisualizationsGetVisualization,
        PathValues.VISUALIZATIONS_GET_MODEL_VISUALIZATIONS: VisualizationsGetModelVisualizations,
        PathValues.VISUALIZATIONS_SAVE_ANALYZER_LAYOUT: VisualizationsSaveAnalyzerLayout,
        PathValues.VISUALIZATIONS_DELETE_VISUALIZATIONS: VisualizationsDeleteVisualizations,
        PathValues.VISUALIZATIONS_GET_STORED_RESOURCE_URL: VisualizationsGetStoredResourceUrl,
    }
)

path_to_api = PathToApi(
    {
        PathValues.AUTH_KEYLOGIN: AuthKeylogin,
        PathValues.AUTH_LOGIN: AuthLogin,
        PathValues.AUTH_KEYGEN: AuthKeygen,
        PathValues.AUTH_WHO_AM_I: AuthWhoAmI,
        PathValues.AUTH_SIGNUP: AuthSignup,
        PathValues.AUTH_ACTIVATE: AuthActivate,
        PathValues.AUTH_RESEND_ACTIVATION_MAIL: AuthResendActivationMail,
        PathValues.AUTH_SEND_RESET_PASSWORD_MAIL: AuthSendResetPasswordMail,
        PathValues.AUTH_RESET_PASSWORD: AuthResetPassword,
        PathValues.AUTH_SET_USER_METADATA: AuthSetUserMetadata,
        PathValues.AUTH_REQUEST_TRIAL: AuthRequestTrial,
        PathValues.AUTH_START_TRIAL: AuthStartTrial,
        PathValues.AUTH_EXTEND_TRIAL: AuthExtendTrial,
        PathValues.AUTH_LOGOUT: AuthLogout,
        PathValues.DASHBOARDS_GET_KIBANA_DASHBOARDS: DashboardsGetKibanaDashboards,
        PathValues.DASHBOARDS_GET_PROJECT_DASHBOARDS: DashboardsGetProjectDashboards,
        PathValues.DASHBOARDS_GET_DASHBOARD: DashboardsGetDashboard,
        PathValues.DASHBOARDS_ADD_DASHBOARD: DashboardsAddDashboard,
        PathValues.DASHBOARDS_DELETE_DASHBOARD: DashboardsDeleteDashboard,
        PathValues.DASHBOARDS_UPDATE_DASHBOARD: DashboardsUpdateDashboard,
        PathValues.DASHBOARDS_GET_KIBANA_DASHLET_FIELDS: DashboardsGetKibanaDashletFields,
        PathValues.DASHBOARDS_GET_DASHLET_FIELDS: DashboardsGetDashletFields,
        PathValues.DATASETS_GET_DATASETS: DatasetsGetDatasets,
        PathValues.DATASETS_ADD_DATASET: DatasetsAddDataset,
        PathValues.DATASETS_TRASH_DATASET: DatasetsTrashDataset,
        PathValues.DATASETS_SAVE_DATASET_VERSION: DatasetsSaveDatasetVersion,
        PathValues.DATASETS_MODIFY_DATASET_VERSION_NOTE: DatasetsModifyDatasetVersionNote,
        PathValues.DATASETS_PARSE_DATASET: DatasetsParseDataset,
        PathValues.DATASETS_GET_DATASET_VERSION: DatasetsGetDatasetVersion,
        PathValues.DATASETS_GET_LATEST_DATASET_VERSION: DatasetsGetLatestDatasetVersion,
        PathValues.DATASETS_GET_DATASET_VERSIONS: DatasetsGetDatasetVersions,
        PathValues.DEMOS_GET_DEMOS: DemosGetDemos,
        PathValues.DEMOS_IMPORT_DEMO_PROJECT: DemosImportDemoProject,
        PathValues.DEMOS_SEND_USER_MESSAGE: DemosSendUserMessage,
        PathValues.EXPORTEDMODELS_GET_EXPORTED_MODEL_JOBS: ExportedmodelsGetExportedModelJobs,
        PathValues.EXPORTEDMODELS_GET_STORED_EXPORTED_MODEL_RESOURCE_URL: ExportedmodelsGetStoredExportedModelResourceUrl,
        PathValues.INSIGHTS_GET_MODEL_INSIGHTS: InsightsGetModelInsights,
        PathValues.ISSUES_GET_PROJECT_ISSUES: IssuesGetProjectIssues,
        PathValues.ISSUES_GET_SINGLE_ISSUE: IssuesGetSingleIssue,
        PathValues.ISSUES_UPDATE_ISSUE: IssuesUpdateIssue,
        PathValues.ISSUES_ADD_ISSUE: IssuesAddIssue,
        PathValues.ISSUES_DELETE_ISSUE: IssuesDeleteIssue,
        PathValues.JOBS_GET_JOBS: JobsGetJobs,
        PathValues.JOBS_GET_TRAINING_JOBS: JobsGetTrainingJobs,
        PathValues.JOBS_IS_TRAINING_JOB_RUNNING: JobsIsTrainingJobRunning,
        PathValues.JOBS_GET_ORGANIZATION_JOBS: JobsGetOrganizationJobs,
        PathValues.JOBS_STOP_JOB: JobsStopJob,
        PathValues.JOBS_TERMINATE_JOB: JobsTerminateJob,
        PathValues.JOBS_WARMUP: JobsWarmup,
        PathValues.JOBS_ADD_EXPORT_MODEL_JOB: JobsAddExportModelJob,
        PathValues.JOBS_TRAIN_FROM_SCRATCH: JobsTrainFromScratch,
        PathValues.JOBS_CONTINUE_TRAIN: JobsContinueTrain,
        PathValues.JOBS_TRAIN_FROM_INITIAL_WEIGHTS: JobsTrainFromInitialWeights,
        PathValues.JOBS_EVALUATE: JobsEvaluate,
        PathValues.JOBS_SAMPLE_ANALYSIS: JobsSampleAnalysis,
        PathValues.JOBS_POPULATION_EXPLORATION: JobsPopulationExploration,
        PathValues.JOBS_SAMPLE_SELECTION: JobsSampleSelection,
        PathValues.JOBS_GET_MACHINE_TYPES: JobsGetMachineTypes,
        PathValues.JOBS_SET_MACHINE_TYPE: JobsSetMachineType,
        PathValues.METADATA_GET_MAX_ACTIVE_USERS: MetadataGetMaxActiveUsers,
        PathValues.METADATA_GET_STATISTICS: MetadataGetStatistics,
        PathValues.MODELTESTS_CREATE_MODEL_TEST: ModelTestsCreateModelTest,
        PathValues.MODELTESTS_UPDATE_MODEL_TEST: ModelTestsUpdateModelTest,
        PathValues.MODELTESTS_GET_SINGLE_MODEL_TEST: ModelTestsGetSingleModelTest,
        PathValues.MODELTESTS_GET_ALL_PROJECT_MODEL_TESTS: ModelTestsGetAllProjectModelTests,
        PathValues.MODELTESTS_DELETE_MODEL_TEST: ModelTestsDeleteModelTest,
        PathValues.MODELTESTS_GET_MODEL_TEST_RESULT: ModelTestsGetModelTestResult,
        PathValues.MODELMETRICS_GET_MODEL_EPOCH_LOSS: ModelmetricsGetModelEpochLoss,
        PathValues.MODELMETRICS_GET_XYCHART: ModelmetricsGetXYChart,
        PathValues.MODELMETRICS_GET_HEATMAP_CHART: ModelmetricsGetHeatmapChart,
        PathValues.MODELMETRICS_GET_TABLE_CHART: ModelmetricsGetTableChart,
        PathValues.MODELMETRICS_GET_CONFUSION_METRIC_NAMES: ModelmetricsGetConfusionMetricNames,
        PathValues.MODELMETRICS_GET_BALANCED_ACCURACY: ModelmetricsGetBalancedAccuracy,
        PathValues.MODELMETRICS_GET_F1SCORE: ModelmetricsGetF1Score,
        PathValues.MODELMETRICS_GET_PR_CURVE: ModelmetricsGetPrCurve,
        PathValues.MODELMETRICS_GET_ROC: ModelmetricsGetRoc,
        PathValues.MODELS_GET_MODELS_BY_HASH: ModelsGetModelsByHash,
        PathValues.MODELS_GET_MODELS_BY_VERSION_ID: ModelsGetModelsByVersionId,
        PathValues.MODELS_GET_RECENT_ORGANIZATION_MODELS: ModelsGetRecentOrganizationModels,
        PathValues.MODELS_DELETE_MODEL: ModelsDeleteModel,
        PathValues.MONITOR_HEALTH_CHECK: MonitorHealthCheck,
        PathValues.NOTIFICATIONS_GET_NOTIFICATIONS: NotificationsGetNotifications,
        PathValues.NOTIFICATIONS_SET_USER_NOTIFICATIONS_AS_READ: NotificationsSetUserNotificationsAsRead,
        PathValues.ORGANIZATIONS_GET_ORGANIZATIONS: OrganizationsGetOrganizations,
        PathValues.ORGANIZATIONS_UPDATE_ORGANIZATION_PUBLIC_NAME: OrganizationsUpdateOrganizationPublicName,
        PathValues.ORGANIZATIONS_CREATE_ORGANIZATION: OrganizationsCreateOrganization,
        PathValues.ORGANIZATIONS_DELETE_ORGANIZATION: OrganizationsDeleteOrganization,
        PathValues.ORGANIZATIONS_SET_DEFAULT_ORGANIZATION: OrganizationsSetDefaultOrganization,
        PathValues.PROJECTS_ADD_PROJECT: ProjectsAddProject,
        PathValues.PROJECTS_GET_PROJECTS: ProjectsGetProjects,
        PathValues.PROJECTS_LOAD_MODEL: ProjectsLoadModel,
        PathValues.PROJECTS_DELETE_PROJECT: ProjectsDeleteProject,
        PathValues.PROJECTS_TRASH_PROJECT: ProjectsTrashProject,
        PathValues.PROJECTS_GET_CURRENT_PROJECT_VERSION: ProjectsGetCurrentProjectVersion,
        PathValues.SECRETMANAGER_ADD_SECRET_MANAGER: SecretManagerAddSecretManager,
        PathValues.SECRETMANAGER_TRASH_SECRET_MANAGER: SecretManagerTrashSecretManager,
        PathValues.SECRETMANAGER_GET_SECRET_MANAGER_LIST: SecretManagerGetSecretManagerList,
        PathValues.SECRETMANAGER_UPDATE_SECRET_MANAGER: SecretManagerUpdateSecretManager,
        PathValues.USERS_GET_ORGANIZATION_SLIM_USER_DATA: UsersGetOrganizationSlimUserData,
        PathValues.USERS_GET_ALL_SLIM_USER_DATA: UsersGetAllSlimUserData,
        PathValues.USERS_UPDATE_USER_STATUS: UsersUpdateUserStatus,
        PathValues.USERS_UPDATE_USER_ORGANIZATION: UsersUpdateUserOrganization,
        PathValues.USERS_UPDATE_USER_ROLE: UsersUpdateUserRole,
        PathValues.USERS_UPDATE_USER_NAME: UsersUpdateUserName,
        PathValues.USERS_DELETE_USER_BY_ID: UsersDeleteUserById,
        PathValues.VERSIONS_IMPORT_MODEL: VersionsImportModel,
        PathValues.VERSIONS_ADD_VERSION: VersionsAddVersion,
        PathValues.VERSIONS_LOAD_VERSION: VersionsLoadVersion,
        PathValues.VERSIONS_DELETE_VERSION: VersionsDeleteVersion,
        PathValues.VERSIONS_UPDATE_VERSION: VersionsUpdateVersion,
        PathValues.VERSIONS_GET_PROJECT_SLIM_VERSIONS: VersionsGetProjectSlimVersions,
        PathValues.VERSIONS_GET_UPLOAD_SIGNED_URL: VersionsGetUploadSignedUrl,
        PathValues.VISUALIZATIONS_GET_VISUALIZATION: VisualizationsGetVisualization,
        PathValues.VISUALIZATIONS_GET_MODEL_VISUALIZATIONS: VisualizationsGetModelVisualizations,
        PathValues.VISUALIZATIONS_SAVE_ANALYZER_LAYOUT: VisualizationsSaveAnalyzerLayout,
        PathValues.VISUALIZATIONS_DELETE_VISUALIZATIONS: VisualizationsDeleteVisualizations,
        PathValues.VISUALIZATIONS_GET_STORED_RESOURCE_URL: VisualizationsGetStoredResourceUrl,
    }
)
