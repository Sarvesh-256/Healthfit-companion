import argparse
import csv
import time
import numpy as np
from sklearn.neural_network import MLPClassifier


# Simple dataset copied from modules/ann_fitness.py
X = np.array([
    [18, 3, 3, 8],
    [22, 4, 2, 7],
    [25, 3, 4, 7],
    [30, 2, 6, 6],
    [35, 1, 8, 5],
    [28, 2, 5, 6],
    [21, 4, 2, 8],
    [24, 3, 3, 7]
])

y = np.array([2, 2, 1, 1, 0, 1, 2, 1])


def run_epochs(epochs: int, lr: float, hidden=(5,)):
    classes = np.unique(y)
    model = MLPClassifier(hidden_layer_sizes=hidden, solver='sgd', learning_rate_init=lr,
                          max_iter=1, warm_start=True)

    results = []
    start = time.time()
    for epoch in range(1, epochs + 1):
        model.partial_fit(X, y, classes=classes)
        loss = float(getattr(model, 'loss_', float('nan')))
        acc = model.score(X, y)
        results.append((epoch, loss, acc))
        print(f"Epoch {epoch:4d}: loss={loss:.6f}, acc={acc:.4f}")

    duration = time.time() - start
    out_path = 'tools/epochs_results.csv'
    with open(out_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['epoch', 'loss', 'accuracy'])
        writer.writerows(results)

    print(f"Run complete: {epochs} epochs in {duration:.2f}s. Results saved to {out_path}")
    return results


def main():
    p = argparse.ArgumentParser(description='Run epoch experiments for ANN classifier')
    p.add_argument('--epochs', '-e', type=int, default=100, help='Number of epochs')
    p.add_argument('--lr', type=float, default=0.01, help='Learning rate')
    p.add_argument('--hidden', type=int, nargs='+', default=[5], help='Hidden layer sizes')
    args = p.parse_args()

    hidden = tuple(args.hidden)
    run_epochs(args.epochs, args.lr, hidden)


if __name__ == '__main__':
    main()
