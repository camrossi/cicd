void slackTalk(msg) {
    T = "TQD55T6UF"
    B = "BQ0K1GBGB"
    S= "oVbsstox4mp30MKNgI28d6NR"
    sh "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"${msg}\"}' https://hooks.slack.com/services/$T/$B/$S"
}

void webexTeamsTalk(msg) {
    botId = "Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OL2M0N2M2NjgwLTIxOGUtNGI4My1hNDIxLWE2ODFiMGRlYzdlOQ"
    bearer = "OTA1N2E1NjYtMDU4ZC00OTQ0LTlkMjUtYzk3N2U2ZjI0NzBlZTg3NmE2OWUtMzNl_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
    botName = "cpaggen-jenkins"
    botUsername = "cpaggen-jenkins@webex.bot"
    roomId = "Y2lzY29zcGFyazovL3VzL1JPT00vOWY4MDA4ODAtMDYwNi0xMWVhLWIyNjctZjE5N2Y2Y2NhZWZm"
    sh "curl -X POST -H 'Content-type: application/json' -H 'Authorization: Bearer ${bearer}' --data '{\"roomId\":\"${roomId}\",\"text\":\"${msg}\"}' https://api.ciscospark.com/v1/messages"
}

pipeline {
 agent any
 tools {
    "org.jenkinsci.plugins.terraform.TerraformInstallation" "terraform"
 }

 environment {
    TF_HOME = tool('terraform')
    TF_IN_AUTOMATION = "true"
    PATH = "$TF_HOME:$PATH"
    TF_LOG = "INFO"
 }
 
 stages {
   stage('Git code checkout'){
     steps {
       dir('dev'){
         ansiColor('xterm'){
           slackTalk("ACI-VMware: fetching source from Git")
           git branch: 'master', url: 'http://10.0.76.250/cisco/onprem.git'
         }
       }
     }
   }
 
   stage('Terraform Init for the ACI plan'){
     steps {
       dir('dev/ACI'){
         ansiColor('xterm'){
           slackTalk("ACI-VMware: terraform init ACI")
           sh "terraform init -input=false -upgrade"
           sh "echo \$PWD" 
         }    
       }
     }
   }

   stage('Terraform Init for the VMWARE plan'){
     steps {
       dir('dev/VMWARE'){
         ansiColor('xterm'){
           slackTalk("ACI-VMware: terraform init VMware")
           sh "terraform init -input=false -upgrade"
           sh "echo \$PWD" 
         }    
       }
     }
   }

   stage('Terraform Plan for ACI') {
     steps {
       dir('dev/ACI'){ 
         ansiColor('xterm') {
           slackTalk("ACI-VMware: terraform plan ACI")
           sh 'terraform plan -out=plan'
         }
       }
     }
   }
  
   stage('Apply ACI plan') {
     steps {
       dir('dev/ACI'){
         ansiColor('xterm'){
           slackTalk("ACI-VMware: terraform apply ACI")
           sh 'terraform apply -auto-approve'
         }
       }
     }
   }
   
   stage('Terraform plan for VMware') {
     steps {
       dir('dev/VMWARE'){
         ansiColor('xterm'){
           slackTalk("ACI-VMware: terraform plan VMware")
           sh 'terraform plan -out=plan'
         }
       }
     }
   }
    
   stage('Apply VMware plan') {
     steps {
       script{
         dir('dev/VMWARE'){
           ansiColor('xterm'){
             slackTalk("ACI-VMware: terraform apply VMware")
             sh 'terraform apply -auto-approve'
           }
         }
       }
     }
   }
   
   stage('Launch web server'){
     steps{
       script{
     def client = [:]
     client.name = "1.1.1.100"
     client.host = "1.1.1.100"
     client.allowAnyHosts = true
     def server = [:]
     server.name = "1.1.1.200"
     server.host = "1.1.1.200"
     server.allowAnyHosts = true
     withCredentials([usernamePassword(credentialsId: 'sshUserAccount', passwordVariable: 'password', usernameVariable: 'userName')]) {
         server.user = userName
         server.password = password
         client.user = userName
         client.password = password
         stage("SSH into Web Server") {
           script{
             try {
               timeout(time: 30, unit: 'SECONDS') {
                 slackTalk("ACI-VMware: starting app.py via SSH")
                 sshCommand remote: server, command: '/home/cisco/start_app.sh &' 
               }
             } catch (err){
                 slackTalk("ACI-VMware: SSH timeout activated - testing app.py")
                 def res = sshCommand remote: server, command: 'curl -s http://1.1.1.200:8080/hello'
                 slackTalk(res)
                 if (res.equals("<h1>You have reached the hello page</h1>")){
                   slackTalk("ACI-VMware: server is up and running")
                   // currentBuild.result = 'SUCCESS'
                 } else{
                     slackTalk("ACI-VMware: web site is not up")
                     currentBuild.result = 'FAILURE'
                   }
                   
               }
           }   
         }            
       }
       stage("Validate ACI contract") {
           script{
               slackTalk("ACI-VMware: curl server:8080 from client")
               def res = sshCommand remote: client, command: 'curl -s http://1.1.1.200:8080/hello' 
               slackTalk(res)
               if (res.equals("<h1>You have reached the hello page</h1>")){
                   slackTalk("ACI-VMware: ACI contract is operational")
                   // currentBuild.result = 'SUCCESS'
                 } else{
                     slackTalk("ACI-VMware: ACI contract not allowing 8080")
                     currentBuild.result = 'FAILURE'
                   }
           }
       }
         
     } 
    }
   }

  } 
} 