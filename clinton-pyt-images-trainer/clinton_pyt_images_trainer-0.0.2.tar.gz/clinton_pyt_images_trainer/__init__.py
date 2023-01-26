import torch
import matplotlib.pyplot as plt

def model_train_validate(epochs, model, criterion, optimizer, trainloader, valloader):
    """
    ###############################################
    ########### Self-made function ################
    ###############################################
    ##### Arguments ##########
    :: epochs (int) -> The number of training you need
    :: model -> Your created PyTorch model
    :: criterion -> The loss function you intend to use
    :: optimizer -> The function you will use to update the model weights
    :: trainloader -> Your training dataset
    :: valloader -> Your validation dataset
    """

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("You are working on : ", device)
    train_losses, val_losses = [], []

    print("\nTraining and validation in progress .......\n ")

    model.train()
    training_loss = 0
    for e in range(epochs):
        for images, labels in trainloader:
            images, labels, model = images.to(device), labels.to(device), model.to(device)
            log_preds = model.forward(images)

            optimizer.zero_grad()
            loss = criterion(log_preds, labels)
            loss.backward()
            optimizer.step()

            training_loss += loss.to("cpu").item()

        else:
            model.eval()
            validation_loss = 0
            accuracy = 0

            with torch.no_grad():
                for images, labels in valloader:
                    images, labels, model = images.to(device), labels.to(device), model.to(device)
                    log_preds = model.forward(images)

                    validation_loss += criterion(log_preds, labels)
                    
                    preds = torch.exp(log_preds)
                    top_p, top_class = preds.topk(1, dim=1)
                    equals = top_class == labels.view(*top_class.shape)

                    accuracy += torch.mean(equals.type(torch.FloatTensor))

            train_losses.append(training_loss/len(trainloader))
            val_losses.append(validation_loss.to("cpu")/len(valloader))

            print("Epoch {}/{} ... ".format(e+1, epochs),
                  "Training Loss : {:.3f} ... ".format(training_loss/len(trainloader)),
                  "Test Loss : {:.3f} ... ".format(validation_loss/len(valloader)),
                  "Test Accuracy : {:.3f}".format(accuracy/len(valloader)))
    
    print("\nTraining and validation completed successfully ........ \n")

    # Save our model state dict
    torch.save(model.state_dict(), "saved_model.pth")
    print("\nYour model has been saved successfully..........")
    
    # Plot the learning curve to identify overfitting and underfitting
    
    plt.plot(train_losses, label="Training loss")
    plt.plot(val_losses, label="Validation loss")
    plt.title("Training and Validation Curve")
    plt.xlabel("No. of Epochs")
    plt.ylabel("Loss")
    plt.legend(frameon=False)