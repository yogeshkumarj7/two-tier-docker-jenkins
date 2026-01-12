pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                bat 'docker build -t tasktrack-app .'
            }
        }

        stage('Deploy') {
            steps {
                bat 'docker compose down'
                bat 'docker compose up -d --build'
            }
        }
    }
}

