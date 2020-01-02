import os
from time import sleep 

def get_kubectl_version():
	os.system("echo $(kubectl version | base64 | tr -d '\n') > /home/masternode/clusterbuildcommands/kubectlversion.txt")	
	with open('kubectlversion.txt', 'r') as file:
		kubectl_version = file.read().replace('\n','')
	return(kubectl_version)

def get_masternode_status():
	os.system("kubectl get nodes > /home/masternode/clusterbuildcommands/nodestatus.txt")
	with open('/home/masternode/clusterbuildcommands/nodestatus.txt') as file:
		contents = file.read()
		search_word = str(' Ready')
		if search_word in contents:
			print('***MasterNode is Ready***')
			return
		else:
			print('***Waiting for MasterNode to be Ready, waiting 5 seconds***')
			sleep(5)
			get_masternode_status()

def main():
	print("***Updating package lists***")
	os.system("sudo apt-get update > /dev/null")
	print("Done")
	
	print("***Installing software dependencies***")
	os.system("sudo apt-get install apt-transport-https ca-certificates curl software-properties-common -y > /dev/null")
	print("Done")
	
	print("***Adding Docker GPG key***")
	os.system("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - ")
	
	print("***Adding Docker Repository***")
	os.system("sudo add-apt-repository 'deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable' > /dev/null")
	print("Done")
	
	os.system("sudo apt-get update -y > /dev/null")
	
	print("***Installing Docker***")
	os.system("sudo apt-get install docker-ce=18.06.2~ce~3-0~ubuntu -y > /dev/null")
	print("Done")
	
	print("***Adding Kubernetes GPG key***")
	os.system("curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add - ")
	
	print("***Adding Kubernetes Repository***")
	os.system("echo 'deb http://apt.kubernetes.io/ kubernetes-xenial main' | sudo tee /etc/apt/sources.list.d/kubernetes.list > /dev/null")
	print("Done")
	
	print("***Updating package lists***")
	os.system("sudo apt-get update > /dev/null")
	print("Done")
	
	print("***Installing Kubernetes Version 1.15.4***")
	os.system("sudo apt-get install kubelet=1.15.4-00 kubeadm=1.15.4-00 kubectl=1.15.4-00 -y > /dev/null")
	print("Done")
	
	print("***Initializing Kubernetes Cluster***")
	print("***Note this process may take 1-5 minutes***")
	os.system("sudo kubeadm init --pod-network-cidr=192.168.10.0/16 --apiserver-advertise-address=192.168.10.20 > /dev/null")
	print("Done")
	
	print("***Creating a directory for Kubernetes configurations***")
	os.system("sudo mkdir -p $HOME/.kube")
	print("Done")
	
	print("***Copying Kubernetes configurations***")
	os.system("sudo cp -i /etc/kubernetes/admin.conf /home/masternode/.kube/config")
	print("Done")
	
	print("***Applying permissions***")
	os.system("sudo chown 1000:1000 /home/masternode/.kube/config")
	print("Done")
	
	print("***Installing Weave as the CNI***")
	os.system("kubectl apply -f 'https://cloud.weave.works/k8s/net?k8s-version=%s'" % get_kubectl_version())
	print("Done")

	print("***Checking Master Node Status***")
	os.system(get_masternode_status())

	print("***Joining Worker Nodes to the Cluster***")
	
if __name__ == '__main__':
	main()
