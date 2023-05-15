import logging
import os
import shutil
import subprocess
from dataclasses import dataclass
from os import listdir
from os.path import isfile, join

logger = logging.getLogger("uvicorn")

@dataclass
class StructBase:
    name: str
    stack_name: str
    environment: str
    team: str


@dataclass
class ArtifactFromGit(StructBase):
    git_repo: str
    branch: str
    project_path: str

    def get(self):

        try:
            directory = f"/tmp/{self.stack_name}/{self.environment}/{self.team}/"
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Directory {directory} created successfully")
        except OSError:
            logger.info(f"Directory {directory} can not be created")

        try:
            if os.path.exists(f"{directory}/{self.name}"):
                shutil.rmtree(f"{directory}/{self.name}")

            logger.info(f"Download git repo {self.git_repo} branch {self.branch}")
            os.chdir(directory)

            result = subprocess.run(
                f"git clone --recurse-submodules --branch {self.branch} {self.git_repo} {self.name}",
                shell=True,
                capture_output=True,
                encoding="utf8",
            )

            logger.info(f"Check if variable.tf file exist")

            tfvars_files = [
                f
                for f in listdir(directory)
                if f.endswith(".tfvars") and isfile(join(directory, f))
            ]

            rc = result.returncode
            if rc != 0:
                return {
                    "command": "git",
                    "rc": rc,
                    "tfvars": tfvars_files,
                    "stdout": result.stderr,
                }
            return {
                "command": "git",
                "rc": rc,
                "tfvars": tfvars_files,
                "stdout": result.stdout,
            }
        except Exception as err:
            return {"command": "git", "rc": 1, "tfvars": tfvars_files, "stdout": err}


@dataclass
class ArtifactFromTemplate(StructBase):
    stack_type: str

    def get(self):

        try:
            directory = f"/tmp/{self.stack_name}/{self.environment}/{self.team}/"
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Directory {directory} created successfully")
        except OSError:
            logger.info(f"Directory {directory} can not be created")

        try:
            if os.path.exists(f"{directory}/{self.name}/{self.stack_type}"):
                shutil.rmtree(f"{directory}/{self.name}/{self.stack_type}")

            logger.info(f"Copy template {self.stack_type}")
            shutil.copytree(f"./src/terraform_template/aws/{self.stack_type}", f"{directory}/{self.name}/{self.stack_type}")

            logger.info(f"Check if (stack_type)_variable.tf file exist")

            tfvars_files = [
                f
                for f in listdir(directory)
                if f.endswith(".tfvars") and isfile(join(directory, f))
            ]
            print(tfvars_files)

            # rc = result.returncode
            # if rc != 0:
            #     return {
            #         "command": "template",
            #         "rc": rc,
            #         "tfvars": tfvars_files,
            #         # "stdout": result.stderr,
            #     }
            return {
                "command": "template",
                "rc": 0,
                "tfvars": tfvars_files,
                # "stdout": result.stdout,
            }
        except Exception as err:
            return {"command": "template", "rc": 1, "tfvars": tfvars_files, "stdout": err}
