import torch

def train(model, device, train_dataloader, optimizer, epochs):
    model.train()

    for batch_ids, (seq, classes) in enumerate(train_dataloader):
        classes=classes.type(torch.LongTensor)
        seq, classes=seq.to(device), classes.to(device)
        torch.autograd.set_detect_anomaly(True)     
        optimizer.zero_grad()
        output=model(seq)
        loss = loss_fn(output,classes)            
        loss.backward()
        optimizer.step()

    if(batch_ids + 1) % 2 == 0:
        print("Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
            epochs, batch_ids* len(seq), len(train_dataloader.dataset),
            100. * batch_ids / len(train_dataloader),loss.item()))
        

# Function for model testing.
def test(model, device, test_dataloader):
    model.eval()
    test_loss=0
    correct=0

    with torch.no_grad():
        for seq,classes in test_dataloader:
            seq,classes=seq.to(device), classes.to(device)
            y_hat=model(seq)
            test_loss+=F.nll_loss(y_hat,classes,reduction='sum').item()
            _,y_pred=torch.max(y_hat,1)
            correct+=(y_pred==classes).sum().item()
    
        test_loss/=len(test_dataloader)
        print("\n Test set: Average loss: {:.0f},Accuracy:{}/{} ({:.0f}%)\n".format(
            test_loss,correct, len(test_dataloader.dataset), 100.*correct/len(test_dataloader.dataset)))
        print('='*30)

# Validation function. Essentially identical to the train function but implements a confusion matrix 
# Validation is done on a separate dataset that the model has not seen before.
def validation(model, device, valid_dataloader):
    model.eval()
    test_loss=0
    correct=0
    tp, tn, fp, fn = 0, 0, 0, 0
    
    with torch.no_grad():
        # create confusion matrix here
        for seq,classes in valid_dataloader:
            seq,classes=seq.to(device), classes.to(device)
            y_hat=model(seq)
            test_loss+=F.nll_loss(y_hat,classes, reduction='sum').item()
            _,y_pred=torch.max(y_hat, 1)
            correct+=(y_pred==classes).sum().item()
            tp, tn, fp, fn = confusion_matrix(y_pred, classes, tp, tn, fp, fn)
        test_loss/=len(valid_dataloader)
        print("\n Validation set: Average loss: {:.0f},Accuracy:{}/{} ({:.0f}%)\n".format(
                test_loss,correct,len(valid_dataloader.dataset),100.*correct/len(valid_dataloader.dataset)))
        print('='*30)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall) / (precision + recall)
    print(f"n = {tp + tn + fp + fn}")
    print(f"True positives: {tp}, True negatives: {tn}, False positives: {fp}, False negatives: {fn}")
    print(f"Actual no total: {tn + fp}, actual yes total: {fn + tp}")
    print(f"Predicted no total: {tn + fn}, predicted yes total: {tp + fp}")
    print(f"Precision: {precision}, Recall: {recall}, F1 Score: {f1}")
        

# Used for determing precision, recall, and F1 score in the validation function.
def confusion_matrix(preds, classes, tp=0, tn=0, fp=0, fn=0):
    for pred, cl in zip(preds, classes):
        if pred == 1 and cl == 1:
            tp += 1
        if pred == 0 and cl == 1:
            fn += 1
        if pred ==  1 and cl == 0:
            fp += 1
        if pred == 0 and cl == 0:
            tn += 1
    return tp, tn, fp, fn