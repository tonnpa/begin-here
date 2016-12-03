from foodmap.models import EvaluationPoint

import pandas as pd
import seaborn as sns


def plot_heatmap():
    def get_coordinates_with_scores():
        eval_pts = EvaluationPoint.objects.all()

        data = list()
        for pt in eval_pts:
            data.append((pt.id, pt.location.x, pt.location.y, pt.favorability_score))

        score_df = pd.DataFrame(data, columns=['id', 'x', 'y', 'score'])
        score_df.sort_values(['y', 'x'], inplace=True)
        return score_df

    def dataframe_to_matrix(eval_pts_df):
        matrix = list()
        for name, group in eval_pts_df.groupby('y'):
            matrix.append(group.score)

        return matrix

    score_df = get_coordinates_with_scores()
    matrix = dataframe_to_matrix(score_df)
    sns.heatmap(matrix)
    sns.plt.show()
