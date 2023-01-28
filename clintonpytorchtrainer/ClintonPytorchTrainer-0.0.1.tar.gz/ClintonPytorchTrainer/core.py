"""
    ###############################################
    ########### Self-made Trainer Class ################
    ########### By Clinton Nyaore ###################
    ###############################################
        """

import torch
import matplotlib.pyplot as plt
import time
   
class TrainTestSave:
    def __init__(self, device, epochs, model, criterion, optimizer, trainloader, valloader):
        """
            ##### Arguments ##########
    :: epochs (int) -> The number of training you need
    :: model -> Your created PyTorch model
    :: criterion -> The loss function you intend to use
    :: optimizer -> The function you will use to update the model weights
    :: trainloader -> Your training dataset
    :: valloader -> Your validation dataset
        """
        super().__init__()
        
        self.device = device
        self.epochs = epochs
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.trainloader = trainloader
        self.valloader = valloader

    def model_train_validate(self):
    
        print("\nmodel={}, opt={}(lr={}), epochs={}, device={}\n" \
              .format(type(self.model).__name__, type(self.optimizer).__name__,
               self.optimizer.param_groups[0]["lr"], self.epochs, self.device))

        self.history = {} # This dictionary will collect loss and acc per-epoch like Keras' fit() #
        self.history["train_losses"] = []
        self.history["train_accs"] = []
        self.history["val_losses"] = []
        self.history["val_accs"] = []

        print("\nTraining and validation in progress .......\n ")
        
        import time
        self.start_time = time.time()

        for e in range(self.epochs):

            # Train the model on the train set
            self.model.train()

            self.training_loss = 0.0
            self.train_accuracy = 0.0
            for data, labels in self.trainloader:
                self.data, self.labels, self.model = data.to(self.device), labels.to(self.device), self.model.to(self.device)
                self.log_preds = self.model.forward(self.data)

                self.optimizer.zero_grad()
                self.loss = self.criterion(self.log_preds, self.labels)
                self.loss.backward()
                self.optimizer.step()

                self.training_loss += self.loss.to("cpu").item()

                self.preds = torch.exp(self.log_preds)
                self.top_p, self.top_class = self.preds.topk(1, dim=1)
                self.equals = self.top_class == self.labels.view(*self.top_class.shape)

                self.train_accuracy += torch.mean(self.equals.type(torch.FloatTensor))

            else:

                # Evaluate the model on the test set
                self.model.eval()

                self.validation_loss = 0.0
                self.val_accuracy = 0.0

                with torch.no_grad():
                    for data, labels in self.valloader:
                        self.data, self.labels, self.model = data.to(self.device), labels.to(self.device), self.model.to(self.device)
                        self.log_preds = self.model.forward(self.data)

                        self.validation_loss += self.criterion(self.log_preds, self.labels)

                        self.preds = torch.exp(self.log_preds)
                        self.top_p, self.top_class = self.preds.topk(1, dim=1)
                        self.equals = self.top_class == self.labels.view(*self.top_class.shape)

                        self.val_accuracy += torch.mean(self.equals.type(torch.FloatTensor))

                self.train_loss = self.training_loss/len(self.trainloader)
                self.train_acc = self.train_accuracy/len(self.trainloader)
                self.val_loss = self.validation_loss.to("cpu")/len(self.valloader)
                self.val_acc = self.val_accuracy/len(self.valloader)

                self.history["train_losses"].append(self.train_loss)
                self.history["train_accs"].append(self.train_acc)
                self.history["val_losses"].append(self.val_loss)
                self.history["val_accs"].append(self.val_acc)

                print("Epoch {}/{} ... ".format(e+1, self.epochs),
                      "Train Loss : {:.3f} ... ".format(self.train_loss),
                      "Train Accuracy : {:.3f} ... ".format(self.train_acc),
                      "Test Loss : {:.3f} ... ".format(self.val_loss),
                      "Test Accuracy : {:.3f}".format(self.val_acc))

        print("\nTraining and validation completed successfully ........ \n")

        # End of training loop

        self.end_time = time.time()
        self.total_time = self.end_time - self.start_time
        self.time_per_epoch = self.total_time / self.epochs
        print()
        print("Time total:     {:.3f} sec".format(self.total_time))
        print("Time per epoch: {:.3f} sec".format(self.time_per_epoch))

        # Plot training and validation accuracy curves
        print("\nPlotting the training curves .............. \n")

        self.train_losses = self.history['train_losses']
        self.train_acc = self.history['train_accs']
        self.val_losses = self.history['val_losses']
        self.val_acc = self.history['val_accs']
        self.epochs = range(1, len(self.train_acc) + 1)

        plt.figure(figsize=(25,6))
        plt.subplot(131)
        plt.title("Training & Validation Accuracy Curve")
        plt.plot(self.epochs, self.train_acc, label="Training acc")
        plt.plot(self.epochs, self.val_acc, label="Validation acc")
        plt.xlabel("No. of Epochs")
        plt.ylabel("Training & Validation Acc")
        plt.legend(frameon=False)

        # Plot training and validation loss curve
        plt.subplot(132)
        plt.title("Training & Validation Loss Curve")
        plt.plot(self.epochs, self.train_losses, label="Training loss")
        plt.plot(self.epochs, self.val_losses, label="Validation loss")
        plt.xlabel("No. of Epochs")
        plt.ylabel(" Training & Validation Loss")
        plt.legend(frameon=False)
        plt.show()

        # Saving the model to avoid retraining it 
        
        print("\nSaving your model to avoid retraining it again...........\n")
        self.checkpoint = {"model" : self.model, "state_dict" : self.model.state_dict()}
        
        torch.save(self.checkpoint, "saved_model.pth")
        print("Done")
        
        return None
    
    def load_model(self, filepath):
        
        # Loading your saved model 
        print("Loading your saved model .......... ")
        checkpoint = torch.load(filepath)
        model = checkpoint["model"]
        model.load_state_dict(checkpoint['state_dict'], strict=False)
        model.avgpool = torch.nn.AdaptiveAvgPool2d((6, 6))
        print("Done! Use it now to make predictions! All the best!")

        return model
