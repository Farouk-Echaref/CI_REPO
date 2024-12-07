# CI_REPO

![alt text](gitops_flow.png)

A **Jenkinsfile** is a script that defines a CI/CD pipeline in Jenkins using either **Declarative** or **Scripted** syntax. The main components of a Jenkinsfile are outlined below, focusing on the most commonly used **Declarative Pipeline** syntax.

---

### **1. `pipeline` Block**
The `pipeline` block is the root of a Declarative Pipeline and defines the entire structure of your CI/CD pipeline.

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
    }
}
```

---

### **2. `agent`**
The `agent` block specifies where the pipeline or stage will run (e.g., a Jenkins node or a Docker container).

- **Options**:
  - `any`: Use any available agent.
  - `none`: No global agent; stages must define their agents.
  - Specify a label: Run on a specific Jenkins node with a matching label.
  - Use Docker:
    ```groovy
    agent {
        docker { image 'maven:3.6.3-jdk-11' }
    }
    ```

---

### **3. `stages`**
The `stages` block contains a series of sequential steps. Each stage represents a part of the pipeline.

```groovy
stages {
    stage('Build') {
        steps {
            echo 'Building...'
        }
    }
    stage('Test') {
        steps {
            echo 'Testing...'
        }
    }
    stage('Deploy') {
        steps {
            echo 'Deploying...'
        }
    }
}
```

---

### **4. `steps`**
The `steps` block inside a stage defines the actions to perform (e.g., running shell commands, invoking tools, etc.).

```groovy
steps {
    sh 'echo "Running shell commands..."'
    script {
        def message = 'Hello from the script block!'
        echo message
    }
}
```

---

### **5. `post`**
The `post` block defines actions to execute after the pipeline or a stage finishes, based on the pipeline result.

- **Options**:
  - `always`: Runs regardless of pipeline success or failure.
  - `success`: Runs only if the pipeline succeeds.
  - `failure`: Runs only if the pipeline fails.
  - `unstable`: Runs if the pipeline becomes unstable.

```groovy
post {
    always {
        echo 'Cleaning up...'
    }
    success {
        echo 'Pipeline succeeded!'
    }
    failure {
        echo 'Pipeline failed.'
    }
}
```

---

### **6. `environment`**
The `environment` block defines environment variables accessible to the pipeline.

```groovy
environment {
    BUILD_ENV = 'development'
    API_KEY = credentials('my-credentials-id')
}
```

---

### **7. `parameters`**
The `parameters` block defines input parameters for the pipeline.

```groovy
parameters {
    string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to build')
    booleanParam(name: 'DEPLOY', defaultValue: true, description: 'Deploy after build')
}
```

---

### **8. `options`**
The `options` block defines execution settings for the pipeline.

```groovy
options {
    timeout(time: 30, unit: 'MINUTES')  // Timeout for the pipeline
    buildDiscarder(logRotator(numToKeepStr: '10'))  // Keep only the last 10 builds
}
```

---

### **9. `triggers`**
The `triggers` block defines automated triggers for the pipeline.

```groovy
triggers {
    cron('H 0 * * *')  // Run daily at midnight
    pollSCM('H/5 * * * *')  // Check SCM every 5 minutes
}
```

---

### **10. `tools`**
The `tools` block defines tool versions to use during the pipeline.

```groovy
tools {
    maven 'Maven 3.6.3'
    jdk 'JDK 11'
}
```

---

### **Example Jenkinsfile**
Here’s a complete example:

```groovy
pipeline {
    agent any
    environment {
        BUILD_ENV = 'production'
    }
    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to build')
    }
    stages {
        stage('Build') {
            steps {
                echo "Building branch: ${params.BRANCH}"
                sh 'mvn clean package'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'mvn test'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sh './deploy.sh'
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

This structure ensures flexibility and modularity for CI/CD pipelines in Jenkins.


### Resources:

* Jenkins course: 
- https://www.youtube.com/watch?v=6YZvp2GwT0A&ab_channel=DevOpsJourney

* configure docker agaent:
- https://devopscube.com/docker-containers-as-build-slaves-jenkins/


```markdown
# Docker Agent Templates in Jenkins

**Docker Agent Templates** define reusable configurations for launching Docker containers as build agents in Jenkins. They enable dynamic, ephemeral agent creation for specific job requirements.

## Key Components
1. **Docker Image**: Name of the Docker image to use (e.g., `maven:3.8.5-jdk-11`).
2. **Labels**: Identifiers for jobs to match specific templates.
3. **Remote File System Root**: Directory inside the container for Jenkins files (default: `/home/jenkins`).
4. **Instance Cap**: Max concurrent containers for the template.
5. **Volumes**: Host directories/files to mount in the container.
6. **Environment Variables**: Custom variables (e.g., `JAVA_HOME`).
7. **Additional Arguments**: Extra `docker run` options.
8. **Pull Strategy**: When to pull the image (e.g., **Always**).
9. **Network**: Docker network (e.g., `bridge`, `host`).
10. **Idle Timeout**: Time before idle containers are terminated.
11. **Expose DOCKER_HOST**: Enables container access to the Docker daemon.

## Benefits
- **Flexibility**: Different environments for different jobs.
- **Isolation**: Avoid dependency conflicts.
- **Scalability**: Dynamic agent provisioning.
- **Reusability**: Simplified configuration management.

## Example Pipeline
```groovy
pipeline {
    agent {
        docker {
            label 'maven-agent'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean install'
            }
        }
    }
}
```

This pipeline uses the `maven-agent` template to spin up a container for the job and removes it post-completion.

## Setup
1. Go to **Manage Jenkins** > **Manage Nodes and Clouds** > **Configure Clouds**.
2. Add a **Docker Cloud**.
3. Create a new **Docker Agent Template** with the desired configuration.
4. Save and test by running a job.

```


```markdown
# Running Jenkins in the Background and Stopping It

## **1. Running Jenkins in the Background**
You can run Jenkins in the background using one of the following methods:

### **Method 1: Use `nohup`**
Run Jenkins in the background with `nohup` to ensure it continues running even if the terminal is closed:

```bash
nohup jenkins > jenkins.log 2>&1 &
```

- **Explanation**:
  - `nohup`: Ignores the hangup signal (prevents termination when the terminal closes).
  - `jenkins`: Launches Jenkins.
  - `> jenkins.log`: Redirects output to a log file named `jenkins.log`.
  - `2>&1`: Redirects error output to the same log file.
  - `&`: Runs the command in the background.

### **Method 2: Use `&` Only**
If you don’t need `nohup`, append `&` to the command:

```bash
jenkins > jenkins.log 2>&1 &
```

**Note**: This process will stop if the terminal is closed unless you use tools like `tmux` or `screen`.

---

## **2. Stopping Jenkins**
To stop Jenkins, you need to find its **Process ID (PID)** and terminate it.

### **Step 1: Find the PID**
Run the following command to locate Jenkins' PID:

```bash
ps aux | grep jenkins
```

Example output:

```plaintext
youruser   12345  0.0  1.2 123456 12345 ? S 10:00   0:00 java -jar /usr/share/jenkins/jenkins.war
```

- The first number (`12345`) is the **PID**.

### **Step 2: Kill the Process**
Terminate the Jenkins process using its PID:

```bash
kill 12345
```

If the process does not stop, forcefully kill it with:

```bash
kill -9 12345
```

---

## **3. Verifying Jenkins is Stopped**
Run the following to confirm Jenkins has stopped:

```bash
ps aux | grep jenkins
```

If no relevant output is shown, Jenkins is no longer running.

---

## **4. Automating with Scripts**
You can create scripts to simplify starting and stopping Jenkins.

### **Start Script (`start_jenkins.sh`)**
```bash
#!/bin/bash
nohup jenkins > jenkins.log 2>&1 &
echo "Jenkins started in the background. Logs are in jenkins.log."
```

### **Stop Script (`stop_jenkins.sh`)**
```bash
#!/bin/bash
PID=$(ps aux | grep '[j]enkins' | awk '{print $2}')
if [ -n "$PID" ]; then
  kill "$PID"
  echo "Jenkins stopped."
else
  echo "Jenkins is not running."
fi
```

Make both scripts executable:

```bash
chmod +x start_jenkins.sh stop_jenkins.sh
```

### **Usage**
- Start Jenkins: `./start_jenkins.sh`
- Stop Jenkins: `./stop_jenkins.sh`
```