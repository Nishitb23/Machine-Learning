# -*- coding: utf-8 -*-
"""AutoEncoder.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JLFhZN2snuJSXVxKGbBUtibPdZ5pMc4M
"""

import torch
import torch.nn as nn
import torch.nn.functional as fn
import torchvision
import torch.optim as optim
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

class AutoEncoder(nn.Module):
    def __init__(self):
        super(AutoEncoder, self).__init__()
        n_input = 784
        layer1 = 256
        layer2 = 128
        new_features = 100
        self.encoder1 = nn.Linear(n_input, layer1)
        self.encoder2 = nn.Linear(layer1,layer2)
        self.encoder3 = nn.Linear(layer2, new_features)
        self.decoder1 = nn.Linear(new_features,layer2)
        self.decoder2 = nn.Linear(layer2,layer1)
        self.decoder3 = nn.Linear(layer1,n_input)

    def forward(self, input):
        encoder_output1 = fn.relu(self.encoder1(input))
        encoder_output2 = fn.relu(self.encoder2(encoder_output1))
        encoder_output3 = fn.relu(self.encoder3(encoder_output2))
        feature_map = encoder_output3
        decoder_output1 = fn.relu(self.decoder1(encoder_output3))
        decoder_output2 = fn.relu(self.decoder2(decoder_output1))
        input_new = fn.relu(self.decoder3(decoder_output2))
        return input_new,feature_map

#training the model
def train(model, trainloader, loss_fn, optimizer, n_epochs,device):
  training_loss = 0
  for e in range(n_epochs):
    training_loss = 0
    for images,_ in trainloader:
      input = images.view(-1, 784).to(device)
      optimizer.zero_grad()
      input_new,_ = model(input)
      loss = loss_fn(input_new, input)
      training_loss = training_loss + loss.item()
      loss.backward()
      optimizer.step()
    training_loss = training_loss / len(trainloader)

  return training_loss

def test(model,testloader,loss_fn,device):
  test_loss = 0
  sample_image = []
  sample_recontruction = []
  sample_feature_map = []
  for images,_ in testloader:
    input = images.view(images.shape[0],-1).to(device)
    sample_image = images.view(images.shape[0],28,28)[0]
    input_new,feature_map = model(input)
    test_loss = test_loss + loss_fn(input_new, input)
    input_new = input_new.detach().numpy()[0]
    feature_map = feature_map.detach().numpy()[0]
    sample_recontruction = input_new.reshape(28,28)
    sample_feature_map = feature_map.reshape(10,10)
    
  test_loss = test_loss / len(testloader)

  return test_loss,sample_image,sample_recontruction,sample_feature_map


#setting hyper parameters
batch_samples = 100

# Load and transform data
#transform = transforms.ToTensor()
transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])

trainset = torchvision.datasets.MNIST('/dataset', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_samples, shuffle=True, num_workers=4)

testset = torchvision.datasets.MNIST('/dataset', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_samples, shuffle=True, num_workers=4)

#creating the model object and its parameters
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoEncoder().to(device)
loss_fn = nn.MSELoss()

#testing the model
epochs = [5]
learning_rates = [1e-6,1e-5,1e-4,1e-3,1e-2]
training_loss = []
test_loss = []

for epoch in epochs:
  for learning_rate in learning_rates:
    model = AutoEncoder().to(device)
    optimizer = optim.Adam(model.parameters(), lr= learning_rate)
    training_loss.append(train(model,trainloader,loss_fn,optimizer,epoch,device))
    loss,image,image_new,feature_map = test(model,testloader,loss_fn,device)
    test_loss.append(loss)
    print("epoch: ",epoch)
    print("learning rate: ",learning_rate)
    plt.imshow(image)
    plt.show()
    plt.imshow(image_new)
    plt.show()
    plt.imshow(feature_map)
    plt.show()

plt.plot(learning_rates, training_loss,label='Training Error')
plt.plot(learning_rates, test_loss,label='Test Error')
plt.xlabel('Learning Rate')
plt.ylabel('Error')
plt.title("Error v/s learning rate(for epoch = 5)")
legend = []
legend.append("Training Error")
legend.append("Test Error")
plt.legend(legend, loc='upper right')
plt.show()

epochs = [1,2,3,4,5]
learning_rates = [1e-3]
training_loss = []
test_loss = []

for epoch in epochs:
  for learning_rate in learning_rates:
    model = AutoEncoder().to(device)
    optimizer = optim.Adam(model.parameters(), lr= learning_rate)
    training_loss.append(train(model,trainloader,loss_fn,optimizer,epoch,device))
    loss,image,image_new,feature_map = test(model,testloader,loss_fn,device)
    test_loss.append(loss)
    print("epoch: ",epoch)
    print("learning rate: ",learning_rate)
    plt.imshow(image)
    plt.show()
    plt.imshow(image_new)
    plt.show()
    plt.imshow(feature_map)
    plt.show()

plt.plot(epochs, training_loss,label='Training Error')
plt.plot(epochs, test_loss,label='Test Error')
plt.xlabel('Learning Rate')
plt.ylabel('Error')
plt.title("Error v/s epochs(for learning rate = 1e-3)")
legend = []
legend.append("Training Error")
legend.append("Test Error")
plt.legend(legend, loc='upper right')
plt.show()

class nNet(nn.Module):
    def __init__(self):
        super(nNet, self).__init__()
        n_input = 100
        layer1 = 64
        layer2 = 32
        n_output = 10
        self.hidden1 = nn.Linear(n_input, layer1)
        self.hidden2 = nn.Linear(layer1,layer2)
        self.outLayer = nn.Linear(layer2,n_output)

    def forward(self, input):
        output1 = fn.relu(self.hidden1(input))
        output2 = fn.relu(self.hidden2(output1))
        prediction = self.outLayer(output2)
        return prediction

def trainNet(model,ecd_model,trainloader, loss_fn, optimizer, n_epochs,device):
  training_loss = 0
  for e in range(n_epochs):
    training_loss = 0
    for images,label in trainloader:
      input = images.view(-1, 784).to(device)
      optimizer.zero_grad()
      input_new,feature_map = ecd_model(input)
      prediction = model(feature_map)
      target = torch.nn.functional.one_hot(label.to(device)).to(torch.float32)
      loss = loss_fn(target,prediction)
      training_loss = training_loss + loss.item()
      loss.backward()
      optimizer.step()
    training_loss = training_loss / len(trainloader)
  return training_loss

def testNet(model,ecd_model,testloader,loss_fn,device):
  test_loss = 0
  accuracy = 0
  for images,label in testloader:
    input = images.view(images.shape[0],-1).to(device)
    input_new,feature_map = ecd_model(input)
    prediction = model(feature_map)
    target = torch.nn.functional.one_hot(label.to(device)).to(torch.float32)
    test_loss = test_loss + loss_fn(target, prediction)
    prediction = prediction.detach().numpy()
    label = label.numpy()
    for p in range(prediction.shape[0]):
      if label[p] == np.argmax(prediction[p]):
        accuracy = accuracy +1
  test_loss = test_loss / len(testloader)
  accuracy = accuracy/ len(testloader)
  return test_loss,accuracy

#testing the model
epochs = [5]
learning_rates = [1e-6,1e-5,1e-4,1e-3,1e-2]
training_loss = []
test_loss = []
accuracy = []
net_model = nNet().to(device)

for epoch in epochs:
  for learning_rate in learning_rates:
    net_model = nNet().to(device)
    optimizer = optim.Adam(net_model.parameters(), lr= learning_rate)
    training_loss.append(trainNet(net_model,model,trainloader,loss_fn,optimizer,epoch,device))
    loss,acc = testNet(net_model,model,testloader,loss_fn,device)
    test_loss.append(loss)
    accuracy.append(acc)


plt.plot(learning_rates, training_loss,label='Training Error')
plt.plot(learning_rates, test_loss,label='Test Error')
plt.xlabel('Learning Rate')
plt.ylabel('Error')
plt.title("Error v/s learning rate(for epoch = 5)")
legend = []
legend.append("Training Error")
legend.append("Test Error")
plt.legend(legend, loc='upper right')
plt.show()

plt.plot(learning_rates, accuracy,label='Accuracy')
plt.xlabel('Learning Rate')
plt.ylabel('Accuracy')
plt.title("Accuracy v/s Learning Rate(for epoch = 5)")
plt.show()

epochs = [1,2,3,4,5]
learning_rates = [1e-3]
training_loss = []
test_loss = []
accuracy = []

for epoch in epochs:
  for learning_rate in learning_rates:
    net_model = nNet().to(device)
    optimizer = optim.Adam(net_model.parameters(), lr= learning_rate)
    training_loss.append(trainNet(net_model,model,trainloader,loss_fn,optimizer,epoch,device))
    loss,acc = testNet(net_model,model,testloader,loss_fn,device)
    test_loss.append(loss)
    accuracy.append(acc)

plt.plot(epochs, training_loss,label='Training Error')
plt.plot(epochs, test_loss,label='Test Error')
plt.xlabel('epoch')
plt.ylabel('Error')
plt.title("Error v/s epochs(for learning rate = 1e-3)")
legend = []
legend.append("Training Error")
legend.append("Test Error")
plt.legend(legend, loc='upper right')
plt.show()

plt.plot(epochs, accuracy,label='Accuracy')
plt.xlabel('epoch')
plt.ylabel('Accuracy')
plt.title("Accuracy v/s epochs(for learning rate = 1e-3)")
plt.show()

