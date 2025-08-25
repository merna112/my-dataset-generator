pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'apt-get update && apt-get install -y python3 python3-pip'
                sh 'pip install pandas --break-system-packages'
            }
        }
        stage('Generate Dataset') {
            steps {
                sh 'python3 generate_advanced_repo_dataset.py'
            }
        }
        stage('Archive Dataset') {
            steps {
                archiveArtifacts artifacts: 'cse_evaluation_data/*.json', followSymlinks: false
            }
        }
    }
}
