import graphene

from accounts.schema.mutations import (
    AuthorityUserRegisterMutation,
    AdminUserChangePasswordMutation,
    AdminUserUploadAvatarMutation,
    AdminAuthorityCreateMutation,
    AdminAuthorityUpdateMutation,
    AdminAuthorityDeleteMutation,
    AdminAuthorityUserCreateMutation,
    AdminAuthorityUserUpdateMutation,
    AdminAuthorityUserDeleteMutation,
    AdminInvitationCodeCreateMutation,
    AdminInvitationCodeUpdateMutation,
    AdminInvitationCodeDeleteMutation,
    ResetPasswordRequestMutation,
    ResetPasswordMutation,
)


class Mutation(graphene.ObjectType):
    authority_user_register = AuthorityUserRegisterMutation.Field()
    admin_user_change_password = AdminUserChangePasswordMutation.Field()
    admin_user_upload_avatar = AdminUserUploadAvatarMutation.Field()
    admin_authority_create = AdminAuthorityCreateMutation.Field()
    admin_authority_update = AdminAuthorityUpdateMutation.Field()
    admin_authority_delete = AdminAuthorityDeleteMutation.Field()
    admin_authority_user_create = AdminAuthorityUserCreateMutation.Field()
    admin_authority_user_update = AdminAuthorityUserUpdateMutation.Field()
    admin_authority_user_delete = AdminAuthorityUserDeleteMutation.Field()
    admin_invitation_code_create = AdminInvitationCodeCreateMutation.Field()
    admin_invitation_code_update = AdminInvitationCodeUpdateMutation.Field()
    admin_invitation_code_delete = AdminInvitationCodeDeleteMutation.Field()
    reset_password_request = ResetPasswordRequestMutation.Field()
    reset_password = ResetPasswordMutation.Field()
