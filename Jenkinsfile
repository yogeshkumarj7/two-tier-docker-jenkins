pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yogeshkumarj7/two-tier-docker-jenkins.git'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t tasktrack-app .'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker compose down || true'
                sh 'docker compose up -d --build'
            }
        }
    }
}
