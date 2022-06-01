from email import message
from attr import fields
import graphene
from django.conf import settings
from django.utils.timezone import now
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_jwt.refresh_token.shortcuts import create_refresh_token
from graphql_jwt.shortcuts import get_token
from pkg_resources import require

from accounts.models import InvitationCode, AuthorityUser, Feature, Authority, User
from accounts.types import (
    AdminAuthorityCreateProblem,
    AdminAuthorityCreateResult,
    AdminAuthorityQueryType,
    AdminAuthorityUpdateProblem,
    AdminAuthorityUpdateResult,
    AdminAuthorityUpdateSuccess,
    AdminAuthorityUserUpdateProblem,
    AdminAuthorityUserUpdateResult,
    AdminFieldValidationProblem,
    AdminAuthorityUserCreateProblem,
    AdminAuthorityUserCreateResult,
    AdminAuthorityUserQueryType,
    UserProfileType,
    CheckInvitationCodeType,
    FeatureType,
    AuthorityType,
)
from pagination import DjangoPaginationConnectionField


class Query(graphene.ObjectType):
    me = graphene.Field(UserProfileType)
    check_invitation_code = graphene.Field(
        CheckInvitationCodeType, code=graphene.String(required=True)
    )
    features = graphene.List(FeatureType)
    authorities = DjangoPaginationConnectionField(AuthorityType)
    authority = graphene.Field(AuthorityType, id=graphene.ID(required=True))
    adminAuthorityQuery = DjangoPaginationConnectionField(AdminAuthorityQueryType)
    adminAuthorityUserQuery = DjangoPaginationConnectionField(
        AdminAuthorityUserQueryType
    )

    @staticmethod
    @login_required
    def resolve_me(root, info):
        user = info.context.user
        if hasattr(user, "authorityuser"):
            return user.authorityuser
        return user

    @staticmethod
    def resolve_check_invitation_code(root, info, code):
        invitation = InvitationCode.objects.filter(
            code=code, from_date__lte=now(), through_date__gte=now()
        ).first()
        if invitation:
            return invitation
        raise GraphQLError(f"code {code} not found!")

    @staticmethod
    def resolve_features(root, info):
        return Feature.objects.all()

    @staticmethod
    def resolve_authorities(root, info, **kwargs):
        user = info.context.user
        if not user.is_superuser:
            raise GraphQLError("Permission denied.")
        return Authority.objects.all()

    @staticmethod
    def resolve_authority(root, info, id):
        user = info.context.user
        if not user.is_superuser:
            raise GraphQLError("Permission denied.")
        return Authority.objects.get(id=id)


class AdminAuthorityCreateMutation(graphene.Mutation):
    class Arguments:
        code = graphene.String(required=True)
        name = graphene.String(required=True)

    result = graphene.Field(AdminAuthorityCreateResult)

    @staticmethod
    def mutate(root, info, code, name):
        if Authority.objects.filter(code=code).exists():
            return AdminAuthorityCreateMutation(
                result=AdminAuthorityCreateProblem(
                    fields=[
                        AdminFieldValidationProblem(
                            name="code", message="duplicate code"
                        )
                    ]
                )
            )

        if not name:
            return AdminAuthorityCreateMutation(
                result=AdminAuthorityCreateProblem(
                    fields=[
                        AdminFieldValidationProblem(
                            name="name", message="name must not be empty"
                        )
                    ]
                )
            )

        authority = Authority.objects.create(code=code, name=name)
        return AdminAuthorityCreateMutation(result=authority)


class AdminAuthorityUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        code = graphene.String(required=True)
        name = graphene.String(required=True)

    result = graphene.Field(AdminAuthorityUpdateResult)

    @staticmethod
    def mutate(root, info, id, code, name):
        authority = Authority.objects.get(pk=id)

        if not authority:
            return AdminAuthorityUpdateMutation(
                result=AdminAuthorityUpdateProblem(
                    fields=[], message="Object not found"
                )
            )

        if authority.code != code and Authority.objects.filter(code=code).exists():
            return AdminAuthorityUpdateMutation(
                result=AdminAuthorityUpdateProblem(
                    fields=[
                        AdminFieldValidationProblem(
                            name="code", message="duplicate code"
                        )
                    ]
                )
            )

        if not name:
            return AdminAuthorityUpdateMutation(
                result=AdminAuthorityUpdateProblem(
                    fields=[
                        AdminFieldValidationProblem(
                            name="name", message="name must not be empty"
                        )
                    ]
                )
            )

        authority.code = code
        authority.name = name
        authority.save()

        return AdminAuthorityUpdateMutation(result=authority)


class AdminAuthorityUserCreateMutation(graphene.Mutation):
    class Arguments:
        authority_id = graphene.Int(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        telephone = graphene.String(required=False)

    result = graphene.Field(AdminAuthorityUserCreateResult)

    @staticmethod
    def mutate(
        root,
        info,
        authority_id,
        username,
        password,
        first_name,
        last_name,
        email,
        telephone,
    ):
        if User.objects.filter(username=username).exists():
            return AdminAuthorityUserCreateMutation(
                result=AdminAuthorityUserCreateProblem(
                    fields=[
                        AdminFieldValidationProblem(
                            name="username", message="duplicate username"
                        )
                    ]
                )
            )

        if not first_name:
            return AdminAuthorityUserCreateMutation(
                result=AdminAuthorityUserCreateProblem(
                    fields=[
                        AdminFieldValidationProblem(
                            name="first_name", message="first name must not be empty"
                        )
                    ]
                )
            )

        user = AuthorityUser.objects.create_user(
            authority=Authority.objects.get(pk=authority_id),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=telephone,
        )
        return AdminAuthorityUserCreateMutation(result=user)


class AdminAuthorityUserUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        authority_id = graphene.Int(required=True)
        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        telephone = graphene.String(required=False)

    result = graphene.Field(AdminAuthorityUserUpdateResult)

    @staticmethod
    def mutate(
        root, info, id, authority_id, username, first_name, last_name, email, telephone
    ):
        print(id)
        print(authority_id)
        authorityUser = AuthorityUser.objects.get(pk=id)

        if not authorityUser:
            return AdminAuthorityUserUpdateMutation(
                result=AdminAuthorityUserUpdateProblem(
                    fields=[], message="Object not found"
                )
            )

        if (
            authorityUser.username != username
            and User.objects.filter(username=username).exists()
        ):
            return AdminAuthorityUserUpdateMutation(
                result=AdminAuthorityUserUpdateProblem(
                    fields=[
                        AdminFieldValidationProblem(
                            name="username", message="duplicate username"
                        )
                    ]
                )
            )

        if not first_name:
            return AdminAuthorityUserUpdateMutation(
                result=AdminAuthorityUserUpdateProblem(
                    fields=[
                        AdminFieldValidationProblem(
                            name="first_name", message="first name must not be empty"
                        )
                    ]
                )
            )

        authorityUser.authority = Authority.objects.get(pk=authority_id)
        authorityUser.username = username
        authorityUser.first_name = first_name
        authorityUser.last_name = last_name
        authorityUser.email = email
        authorityUser.telephone = telephone
        authorityUser.save()
        return AdminAuthorityUserUpdateMutation(result=authorityUser)


class AuthorityUserRegisterMutation(graphene.Mutation):
    class Arguments:
        invitation_code = graphene.String(required=True)
        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        telephone = graphene.String(required=False)
        email = graphene.String(required=True)

    me = graphene.Field(UserProfileType)
    # return only when enable FEATURES.AUTO_LOGIN_AFTER_REGISTER
    token = graphene.String(required=False)
    refresh_token = graphene.String(required=False)

    @staticmethod
    def mutate(
        root,
        info,
        invitation_code,
        username,
        first_name,
        last_name,
        email,
        telephone=None,
    ):
        invitation = InvitationCode.objects.filter(code=invitation_code).first()
        if invitation:
            if AuthorityUser.objects.filter(username=username).exists():
                raise GraphQLError(f"username {username} already exist")
            authority_user = AuthorityUser.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                telephone=telephone,
                email=email,
                authority=invitation.authority,
            )

            token = None
            refresh_token = None
            if settings.AUTO_LOGIN_AFTER_REGISTER:
                token = get_token(authority_user)
                refresh_token = create_refresh_token(authority_user)

            return AuthorityUserRegisterMutation(
                me=authority_user, token=token, refresh_token=refresh_token
            )
        else:
            raise GraphQLError(f"invitation code {invitation_code} does not exist")


class Mutation(graphene.ObjectType):
    authority_user_register = AuthorityUserRegisterMutation.Field()
    admin_authority_create = AdminAuthorityCreateMutation.Field()
    admin_authority_update = AdminAuthorityUpdateMutation.Field()
    admin_authority_user_create = AdminAuthorityUserCreateMutation.Field()
    admin_authority_user_update = AdminAuthorityUserUpdateMutation.Field()
