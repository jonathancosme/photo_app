from scripts.config import default_folder, plot_size, plot_style, max_photos, default_random_seed, img_extensions
from scripts.functions import is_file_an_img
import streamlit as st
import matplotlib.pyplot as plt
import PIL
import os
import numpy as np

plt.style.use(plot_style)
plt.rcParams["figure.figsize"] = plot_size

def write():

    folder_path = st.text_input("Enter the file directory of images",
                                value=default_folder,
                               key='folder_path',
                               )

    all_available_photos = os.listdir(folder_path)
    all_available_photos = [a_file for a_file in all_available_photos if is_file_an_img(a_file)]


    selection_type = st.selectbox('Do you want to select your photos randomly, or manually?',
                                  options=['random', 'manual'],
                                  index=0,
                                  key='selection_type')

    if selection_type == 'random':
        n_photos_to_select = st.number_input(
            f"Enter number of photos to randomly select (limit is {max_photos} images)",
            min_value=1,
            max_value=max_photos,
            value=1,
            step=1,
            key='n_photos_to_select',
            )
        n_photos_to_select = int(n_photos_to_select)
        use_seed = st.checkbox('Use random seed?',
                               value=True,
                               key='use_seed',
                               )
        if use_seed:
            random_seed = st.number_input(f"Enter a random seed)",
                                          value=default_random_seed,
                                          step=1,
                                          key='random_seed',
                                          )
            random_seed = int(random_seed)
            np.random.seed(random_seed)
            randomly_selected_img_files = np.random.choice(all_available_photos, replace=False,
                                                           size=n_photos_to_select).tolist()
            selected_img_files = randomly_selected_img_files

        else:
            randomly_selected_img_files = np.random.choice(all_available_photos, replace=False,
                                                           size=n_photos_to_select).tolist()
            selected_img_files = randomly_selected_img_files

    else:
        selected_img_files = st.multiselect(f"Select images to load (limit is {max_photos} images)",
                                            options=all_available_photos,
                                            key='selected_img_files',
                                            )


    selected_img_files = [folder_path + '/' + a_file for a_file in selected_img_files]

    if st.button('Show images'):
        if len(selected_img_files) > max_photos:
            st.write(f"Please select {max_photos} or less images")
        else:
            n_photos = len(selected_img_files)
            plot_ncols = np.ceil(np.sqrt(n_photos)).astype(int)
            plot_nrows = np.ceil(n_photos / plot_ncols).astype(int)
            fig = plt.figure()
            st.write(plot_ncols)
            st.write(plot_nrows)
            for num, x in enumerate(selected_img_files):
                # st.write(x.split('/')[-1].split('.')[0])
                img = PIL.Image.open(x)
                ax = fig.add_subplot(plot_nrows, plot_ncols, num+1)
                ax.set_title(x.split('/')[-1], size=30)
                ax.axis('off')
                ax.imshow(img)
            st.pyplot(fig)



if __name__ == "__main__":
    write()