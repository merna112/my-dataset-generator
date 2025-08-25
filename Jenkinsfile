pipeline {
    agent any

    stages {
        stage('Generate Dataset') {
            steps {
                sh 'python3 generate_dataset.py'
            }
        }

        stage('Archive Dataset') {
            steps {
                archiveArtifacts artifacts: 'service_discovery_dataset.json', fingerprint: true
            }
        }
    }
}
