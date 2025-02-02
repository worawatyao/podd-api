import graphene

from .mutations import (
    AdminCaseDefinitionCreateMutation,
    AdminCaseDefinitionUpdateMutation,
    AdminCaseDefinitionDeleteMutation,
    AdminStateDefinitionCreateMutation,
    AdminStateDefinitionUpdateMutation,
    AdminStateDefinitionDeleteMutation,
    AdminStateStepCreateMutation,
    AdminStateStepUpdateMutation,
    AdminStateStepDeleteMutation,
    AdminStateTransitionCreateMutation,
    AdminStateTransitionUpdateMutation,
    AdminStateTransitionDeleteMutation,
    AdminNotificationTemplateCreateMutation,
    AdminNotificationTemplateUpdateMutation,
    AdminNotificationTemplateDeleteMutation,
    AdminAuthorityNotificationUpsertMutation,
    PromoteToCaseMutation,
    ForwardStateMutation,
)


class Mutation(graphene.ObjectType):
    promote_to_case = PromoteToCaseMutation.Field()
    admin_case_definition_create = AdminCaseDefinitionCreateMutation.Field()
    admin_case_definition_update = AdminCaseDefinitionUpdateMutation.Field()
    admin_case_definition_delete = AdminCaseDefinitionDeleteMutation.Field()
    admin_state_definition_create = AdminStateDefinitionCreateMutation.Field()
    admin_state_definition_update = AdminStateDefinitionUpdateMutation.Field()
    admin_state_definition_delete = AdminStateDefinitionDeleteMutation.Field()
    admin_state_step_create = AdminStateStepCreateMutation.Field()
    admin_state_step_update = AdminStateStepUpdateMutation.Field()
    admin_state_step_delete = AdminStateStepDeleteMutation.Field()
    admin_state_transition_create = AdminStateTransitionCreateMutation.Field()
    admin_state_transition_update = AdminStateTransitionUpdateMutation.Field()
    admin_state_transition_delete = AdminStateTransitionDeleteMutation.Field()
    admin_notification_template_create = AdminNotificationTemplateCreateMutation.Field()
    admin_notification_template_update = AdminNotificationTemplateUpdateMutation.Field()
    admin_notification_template_delete = AdminNotificationTemplateDeleteMutation.Field()
    admin_authority_notification_upsert = (
        AdminAuthorityNotificationUpsertMutation.Field()
    )
    forward_state = ForwardStateMutation.Field()
