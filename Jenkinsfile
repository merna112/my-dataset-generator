pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('github_token')
    }

    stages {
        stage('Setup venv') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Fetch Data from GitHub') {
            steps {
                sh '''
                    . venv/bin/activate
                    python fetch_github_data.py
                '''
            }
        }

        stage('Build Dataset') {
            steps {
                sh '''
                    . venv/bin/activate
                    python build_dataset.py
                '''
            }
        }

        stage('Archive Dataset') {
            steps {
                archiveArtifacts artifacts: 'service_discovery_dataset.json', fingerprint: true
            }
        }
    }
}
