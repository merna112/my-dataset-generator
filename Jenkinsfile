pipeline {
    agent any

    stages {
        stage('1. Preparing Environment') {
            steps {
                echo 'Installing necessary Python libraries...'
                sh 'pip install pandas'
            }
        }
        stage('2. Generating Smart Dataset') {
            steps {
                echo 'Executing the advanced dataset generation script...'
                sh 'python generate_advanced_repo_dataset.py'
            }
        }
        stage('3. Archiving Results') {
            steps {
                echo 'Saving the generated dataset as a build artifact...'
                archiveArtifacts artifacts: 'advanced_evaluation_data/*.csv', followSymlinks: false
            }
        }
    }
    post {
        success {
            echo 'Pipeline finished successfully. Dataset is ready.'
        }
        failure {
            echo 'Pipeline failed. Please check the console output.'
        }
    }
}
