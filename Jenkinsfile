pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                powershell '''
                python -m venv .venv
                .\\.venv\\Scripts\\python.exe -m pip install --upgrade pip
                .\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt pytest
                '''
            }
        }

        stage('Run tests') {
            steps {
                powershell '''
                .\\.venv\\Scripts\\python.exe -m pytest -v
                '''
            }
        }
    }
}