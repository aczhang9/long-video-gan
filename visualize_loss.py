import pandas as pd
import matplotlib.pyplot as plt
import click

def plotStats(jsonl_file, training_stats):
    jsonObj = pd.read_json(path_or_buf=jsonl_file, lines=True)

    ticks = []
    for i in range(0,len(jsonObj)):
        ticks.append(jsonObj['progress/tick'][i].get('mean'))
    
    # plot lines
    for stat in training_stats:
        stat_val = []
        for i in range(0, len(jsonObj)):
            stat_val.append(jsonObj[stat][i].get('mean'))
        plt.plot(ticks, stat_val, label = "{}".format(stat.split('/')[1]))
    plt.xlabel("Ticks")
    plt.ylabel("Loss")
    plt.title("Training Pink Flowers")
    plt.legend()
    plt.savefig('flower_pink_loss.png')
    plt.show()
    

###########################################################################################################
@click.command()
@click.option("--file", "-f", "jsonl_file", help="Path to stats.jsonl file", type=str, required=True, multiple=False)
@click.option("--stats", "-s", "training_stats", help="Stats metrics to plot. Options: loss/G_score, loss/G_sign, loss/G_loss, loss/D_score_fake, loss/D_score_real, loss/D_sign_fake, loss/D_sign_real, loss/D_loss, loss/r1_penalty, loss/r1_loss", \
                                                default=['loss/G_loss', 'loss/D_loss'], type=str, multiple=True)
def main(
    jsonl_file: str,
    training_stats: int,
):
    """
    Plot training stats
    python visualize_loss.py -f runs/lres/00023-flower_pink-4batch-4accum-1.0gamma/stats.jsonl
    """
    plotStats(jsonl_file, training_stats)

###########################################################################################################

if __name__ == "__main__":
    main()
    