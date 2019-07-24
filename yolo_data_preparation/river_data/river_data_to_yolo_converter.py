import numpy as np
import pandas as pd


def reformat_river_data(input_file_name, output_file_name, img_path_head):
    df = pd.read_csv(input_file_name)
    img_list = list(df['filename'].unique())
    cnt = 0

    with open(output_file_name, 'w', newline='') as myfile:

        for img in img_list:
            curr_df = df[df['filename'] == img]

            row = curr_df.iloc[[0]]

            content_list = ""
            content_list += str(cnt) + " "

            content_list += img_path_head + img.replace(' ', '_') + " "
            content_list += str(row['width'].values[0]) + " "
            content_list += str(row['height'].values[0]) + " "

            cnt += 1
            for i in range(curr_df.shape[0]):
                box_i = ""
                row = curr_df.iloc[[i]]

                if str(row['class'].values[0]) == 'plastic':
                    label = 0
                else:
                    raise Exception('unrecognized class')

                if i == curr_df.shape[0] - 1:
                    box_i += str(label) + " " + str(row['xmin'].values[0]) + " " + str(
                        row['ymin'].values[0]) + " " + str(row['xmax'].values[0]) + " " + str(row['ymax'].values[0])
                else:
                    box_i += str(label) + " " + str(row['xmin'].values[0]) + " " + str(
                        row['ymin'].values[0]) + " " + str(row['xmax'].values[0]) + " " + str(
                        row['ymax'].values[0]) + " "

                content_list += box_i

            myfile.write(content_list + "\n")

if __name__=='__main__':
    reformatted_data = reformat_river_data('test_labels.csv', 'test.txt', '')
