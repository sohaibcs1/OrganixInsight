# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import json
# from sklearn.preprocessing import MinMaxScaler
# import base64
# import io

# def normalize_row(row):
#     mean_val = row.mean()
#     std_val = row.std()
#     return (row - mean_val) / (std_val)

# def generate_and_plot(json_strings, labels):
#     # Load JSON strings into a list of dictionaries
#     data_list = [json.loads(json_str) for json_str in json_strings]

#     # Find all unique keys across all JSON objects
#     all_keys = set()
#     for data in data_list:
#         all_keys.update(data.keys())

#     # Ensure all dictionaries have the same keys, adding missing keys with a default value (e.g., 0)
#     for data in data_list:
#         for key in all_keys:
#             if key not in data:
#                 data[key] = 0  # Default value can be set to None, 0, or any other value suitable for your context

#     # Convert to DataFrame
#     input_data = pd.DataFrame(data_list)
#     #Specify which columns to normalize (assuming 'Elongation of Colony' and 'Flatness of Colony')
#     # columns_to_normalize = ['Nuclear Volume','Colony total Cells','Colony Diameter','Colony Radius','Max Neighbourhood Distance','Mean Neighbourhood Distance','Elongation of Colony', 'Flatness of Colony','Lumen Volume','Volume of Colony Convex Hull']

#     #mean of 0 and a standard deviation of 1,
#     input_data=input_data.T
#     input_data.columns=labels
#     # scaler = MinMaxScaler()
#     input_data_normalized = input_data.apply(normalize_row,axis=1)


#     # Plot clustermap with normalization
#     plt.figure(figsize=(12, 10))
#     # sns.clustermap(input_data_normalized, annot=True, cmap='vlag', standard_scale=None)
#     sns.clustermap(
#     input_data_normalized,
#     annot=True,
#     cmap='vlag',
#     standard_scale=None,
#     annot_kws={"fontsize": 11, "fontweight": "bold"},  # Adjust font size and make bold
#     figsize=(14, 12)  # Set figure size
#     )


#     # Save the plot to a bytes buffer
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)

#     # Encode the buffer to base64
#     img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

#     # Close the plot
#     plt.close()

#     return img_base64

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import base64
import io

def normalize_row(row):
    mean_val = row.mean()
    std_val = row.std()
    return (row - mean_val) / (std_val)

def generate_and_plot(json_strings, labels):
    # Load JSON strings into a list of dictionaries
    data_list = [json.loads(json_str) for json_str in json_strings]

    # Find all unique keys across all JSON objects
    all_keys = set()
    for data in data_list:
        all_keys.update(data.keys())

    # Ensure all dictionaries have the same keys, adding missing keys with a default value (e.g., 0)
    for data in data_list:
        for key in all_keys:
            if key not in data:
                data[key] = 0  # Default value can be set to None, 0, or any other value suitable for your context

    # Convert to DataFrame
    input_data = pd.DataFrame(data_list)

    # Transpose and assign labels as column names
    input_data = input_data.T
    input_data.columns = labels

    # Normalize the data with mean of 0 and standard deviation of 1
    input_data_normalized = input_data.apply(normalize_row, axis=1)

    # Plot clustermap with customization
    plt.figure(figsize=(12, 11))
    heatmap = sns.clustermap(
        input_data_normalized,
        annot=True,
        cmap='vlag',
        standard_scale=None,
        tree_kws=dict(linewidths=3, colors=(0.2, 0.2, 0.4)),
        annot_kws={"fontsize": 16, "fontweight": "bold"},  # Adjust font size and make bold
        figsize=(16, 16),  # Set figure size,

    )

    # Customize x and y axes font properties
    heatmap.ax_heatmap.set_xlabel('', fontsize=12, fontweight='bold')
    heatmap.ax_heatmap.set_ylabel('', fontsize=12, fontweight='bold')

    # Customize tick label font size and weight for x and y axes
    heatmap.ax_heatmap.tick_params(
        axis='x',
        labelsize=22,
        rotation=90
    )

    heatmap.ax_heatmap.tick_params(
        axis='y',
        labelsize=22
    )

    for tick in heatmap.ax_heatmap.get_xticklabels():
        tick.set_fontweight('bold')
        tick.set_rotation(90)
        tick.set_horizontalalignment('center')
        tick.set_verticalalignment('top')

    for tick in heatmap.ax_heatmap.get_yticklabels():
        tick.set_fontweight('bold')


    heatmap.cax.tick_params(labelsize=18)
    # heatmap.cax.set_title("Scale", fontsize=12, fontweight='bold', loc='left')  # Title at top-left of color bar

    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)

    # Encode the buffer to base64
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Close the plot
    plt.close()

    return img_base64
