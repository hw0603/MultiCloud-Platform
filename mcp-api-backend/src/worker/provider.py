# DI terraform provider
from src.worker.providers.hashicorp.actions import Actions, SimpleActions
from src.worker.providers.hashicorp.artifact import *
from src.worker.providers.hashicorp.download import BinaryDownload
from src.worker.providers.hashicorp.templates import Backend, GetVars, Tfvars


class ProviderRequirements:
    """
    ProviderActions가 실행되기 위해 필요한 모든 것들을 생성하는 클래스
    """

    # terraform binary 다운로드
    def binary_download(version, binary=BinaryDownload):
        config_binary = binary(version)
        return config_binary.get()

    # git repo에서 tf 파일 다운로드
    def artifact_download(
        name: str,
        stack_name: str,
        environment: str,
        team: str,
        git_repo: str,
        branch: str,
        project_path: str = "",
        artifact=ArtifactFromGit,
    ) -> dict:
        config_artifact = artifact(
            name, stack_name, environment, team, git_repo, branch, project_path
        )
        return config_artifact.get()
    
    # 내부 tf 템플릿 파일 복사
    def artifact_copy(
        name: str,
        stack_name: str,
        stack_type: str,
        csp_type: str,
        environment: str,
        team: str,
        artifact=ArtifactFromTemplate,
    ) -> dict:
        config_artifact = artifact(
            name, stack_name, environment, team, stack_type, csp_type
        )
        return config_artifact.get()

    def storage_state(
        name: str,
        stack_name: str,
        environment: str,
        team: str,
        project_path: str,
        backend=Backend,
    ) -> dict:
        config_backend = backend(name, stack_name, environment, team, project_path)
        return config_backend.save()

    def parameter_vars(
        name: str,
        stack_name: str,
        environment: str,
        team: str,
        project_path: str,
        kwargs: dict,
        vars=Tfvars,
    ) -> dict:
        config_vars = vars(name, stack_name, environment, team, project_path, kwargs)
        return config_vars.save()


class ProviderGetVars:
    """
    provider vairables에서 정보를 얻기 위한 클래스
    """

    def json_vars(
        name: str,
        stack_name: str,
        stack_type: str,
        csp_type: str,
        environment: str,
        team: str,
        project_path: str="",
        vars=GetVars,
    ) -> dict:
        config_vars = vars(name, stack_name, stack_type, csp_type, environment, team, project_path)
        return config_vars.get_vars_json()


class ProviderActions:
    """
    terraform deploy 시 각 action에 대응되는 메소드를 가지고 있는 클래스
    """

    # terraform plan
    def plan(
        name: str,
        stack_name: str,
        branch: str,
        environment: str,
        team: str,
        version: str,
        secreto: dict,
        variables_file: str = "",
        project_path: str = "",
        action=Actions,
    ) -> dict:
        config_action = action(
            name,
            stack_name,
            branch,
            environment,
            team,
            version,
            secreto,
            variables_file,
            project_path,
        )
        return config_action.plan_execute()

    # terraform apply
    def apply(
        name: str,
        stack_name: str,
        branch: str,
        environment: str,
        team: str,
        version: str,
        secreto: dict,
        variables_file: str = "",
        project_path: str = "",
        action=Actions,
    ) -> dict:
        config_action = action(
            name,
            stack_name,
            branch,
            environment,
            team,
            version,
            secreto,
            variables_file,
            project_path,
        )
        return config_action.apply_execute()

    # terraform destroy
    def destroy(
        name: str,
        stack_name: str,
        branch: str,
        environment: str,
        team: str,
        version: str,
        secreto: dict,
        variables_file: str = "",
        project_path: str = "",
        action=Actions,
    ) -> dict:
        config_action = action(
            name,
            stack_name,
            branch,
            environment,
            team,
            version,
            secreto,
            variables_file,
            project_path,
        )
        return config_action.destroy_execute()

    # terraform output
    def output(
        stack_name: str, team: str, environment: str, name: str, action=SimpleActions
    ) -> dict:
        config_action = action(stack_name, team, environment, name)
        return config_action.output_execute()

    def unlock(
        stack_name: str, team: str, environment: str, name: str, action=SimpleActions
    ) -> dict:
        config_action = action(stack_name, team, environment, name)
        return config_action.unlock_execute()

    # terraform show
    def show(
        stack_name: str, team: str, environment: str, name: str, action=SimpleActions
    ) -> dict:
        config_action = action(stack_name, team, environment, name)
        return config_action.show_execute()
