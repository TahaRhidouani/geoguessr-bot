import sys
import pathlib
import numpy as np
import tensorflow as tf

tf.get_logger().setLevel('ERROR')

IMG_HEIGHT = int(662)
IMG_WIDTH = int(1136)
COUNTRIES = ['Aland', 'Albania', 'American Samoa', 'Andorra', 'Antarctica', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Bangladesh', 'Belarus', 'Belgium', 'Bermuda', 'Bhutan', 'Bolivia', 'Botswana', 'Brazil', 'Bulgaria', 'Cambodia', 'Canada', 'Chile', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Curacao', 'Czechia', 'Denmark', 'Dominican Republic', 'Ecuador', 'Egypt', 'Estonia', 'Eswatini', 'Faroe Islands', 'Finland', 'France', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Guam', 'Guatemala', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Japan', 'Jersey', 'Jordan', 'Kenya', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Lithuania', 'Luxembourg', 'Macao', 'Madagascar', 'Malaysia', 'Malta', 'Martinique', 'Mexico', 'Monaco', 'Mongolia', 'Montenegro', 'Mozambique', 'Myanmar', 'Nepal', 'Netherlands', 'New Zealand', 'Nigeria', 'North Macedonia', 'Northern Mariana Islands', 'Norway', 'Pakistan', 'Palestine', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn Islands', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 'San Marino', 'Senegal', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Georgia and South Sandwich Islands', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Svalbard and Jan Mayen', 'Sweden', 'Switzerland', 'Taiwan', 'Tanzania', 'Thailand', 'Tunisia', 'Turkey', 'US Virgin Islands', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Venezuela', 'Vietnam']
COORDINATES = {'Andorra': (42.546245, 1.601554), 'United Arab Emirates': (23.424076, 53.847818), 'Albania': (41.153332, 20.168331), 'Armenia': (40.069099, 45.038189), 'Antarctica': (-75.250973, -0.071389), 'Argentina': (-38.416097, -63.616672), 'American Samoa': (-14.270972, -170.132217), 'Austria': (47.516231, 14.550072), 'Australia': (-25.274398, 133.775136), 'Bangladesh': (23.684994, 90.356331), 'Belgium': (50.503887, 4.469936), 'Bulgaria': (42.733883, 25.48583), 'Bermuda': (32.321384, -64.75737), 'Bolivia': (-16.290154, -63.588653), 'Brazil': (-14.235004, -51.92528), 'Bhutan': (27.514162, 90.433601), 'Botswana': (-22.328474, 24.684866), 'Belarus': (53.709807, 27.953389), 'Canada': (56.130366, -106.346771), 'Switzerland': (46.818188, 8.227512), 'Chile': (-35.675147, -71.542969), 'China': (35.86166, 104.195397), 'Colombia': (4.570868, -74.297333), 'Costa Rica': (9.748917, -83.753428), 'Germany': (51.165691, 10.451526), 'Denmark': (56.26392, 9.501785), 'Dominican Republic': (18.735693, -70.162651), 'Ecuador': (-1.831239, -78.183406), 'Estonia': (58.595272, 25.013607), 'Egypt': (26.820553, 30.802498), 'Spain': (40.463667, -3.74922), 'Finland': (61.92411, 25.748151), 'Faroe Islands': (61.892635, -6.911806), 'France': (46.227638, 2.213749), 'United Kingdom': (55.378051, -3.435973), 'Ghana': (7.946527, -1.023194), 'Gibraltar': (36.137741, -5.345374), 'Greenland': (71.706936, -42.604303), 'Greece': (39.074208, 21.824312), 'Guatemala': (15.783471, -90.230759), 'Guam': (13.444304, 144.793731), 'Hong Kong': (22.396428, 114.109497), 'Croatia': (45.1, 15.2), 'Hungary': (47.162494, 19.503304), 'Indonesia': (-0.789275, 113.921327), 'Ireland': (53.41291, -8.24389), 'Israel': (31.046051, 34.851612), 'Isle of Man': (54.236107, -4.548056), 'India': (20.593684, 78.96288), 'Iraq': (33.223191, 43.679291), 'Iceland': (64.963051, -19.020835), 'Italy': (41.87194, 12.56738), 'Jersey': (49.214439, -2.13125), 'Jordan': (30.585164, 36.238414), 'Japan': (36.204824, 138.252924), 'Kenya': (-0.023559, 37.906193), 'Kyrgyzstan': (41.20438, 74.766098), 'Cambodia': (12.565679, 104.990963), 'South Korea': (35.907757, 127.766922), 'Laos': (19.85627, 102.495496), 'Lebanon': (33.854721, 35.862285), 'Sri Lanka': (7.873054, 80.771797), 'Lesotho': (-29.609988, 28.233608), 'Lithuania': (55.169438, 23.881275), 'Luxembourg': (49.815273, 6.129583), 'Latvia': (56.879635, 24.603189), 'Monaco': (43.750298, 7.412841), 'Montenegro': (42.708678, 19.37439), 'Madagascar': (-18.766947, 46.869107), 'Mongolia': (46.862496, 103.846656), 'Northern Mariana Islands': (17.33083, 145.38469), 'Martinique': (14.641528, -61.024174), 'Malta': (35.937496, 14.375416), 'Mexico': (23.634501, -102.552784), 'Malaysia': (4.210484, 101.975766), 'Mozambique': (-18.665695, 35.529562), 'Nigeria': (9.081999, 8.675277), 'Netherlands': (52.132633, 5.291266), 'Norway': (60.472024, 8.468946), 'Nepal': (28.394857, 84.124008), 'New Zealand': (-40.900557, 174.885971), 'Peru': (-9.189967, -75.015152), 'Philippines': (12.879721, 121.774017), 'Pakistan': (30.375321, 69.345116), 'Poland': (51.919438, 19.145136), 'Pitcairn Islands': (-24.703615, -127.439308), 'Puerto Rico': (18.220833, -66.590149), 'Portugal': (39.399872, -8.224454), 'Paraguay': (-23.442503, -58.443832), 'Qatar': (25.354826, 51.183884), 'Romania': (45.943161, 24.96676), 'Serbia': (44.016521, 21.005859), 'Russia': (55.7558, 37.6173), 'Sweden': (60.128161, 18.643501), 'Singapore': (1.352083, 103.819836), 'Slovenia': (46.151241, 14.995463), 'Svalbard and Jan Mayen': (77.553604, 23.670272), 'Slovakia': (48.669026, 19.699024), 'San Marino': (43.94236, 12.457777), 'Senegal': (14.497401, -14.452362), 'Thailand': (15.870032, 100.992541), 'Tunisia': (33.886917, 9.537499), 'Turkey': (38.963745, 35.243322), 'Taiwan': (23.69781, 120.960515), 'Tanzania': (-6.369028, 34.888822), 'Ukraine': (48.379433, 31.16558), 'Uganda': (1.373333, 32.290275), 'United States': (37.09024, -95.712891), 'Uruguay': (-32.522779, -55.765835), 'Venezuela': (6.42375, -66.58973), 'Vietnam': (14.058324, 108.277199), 'South Africa': (-30.559482, 22.937506), 'US Virgin Islands': (18.335765, -64.896335), 'South Sudan': (12.862807, 30.217636), 'South Georgia and South Sandwich Islands': (-54.429579, -36.587909), 'Reunion': (-21.115141, 55.536384), 'Palestine': (31.046051, 34.851612), 'North Macedonia': (41.608635, 21.745275), 'Myanmar': (21.913965, 95.956223), 'Macao': (22.198745, 113.543873), 'Eswatini': (26.5225, 31.4659), 'Czechia': (49.817492, 15.472962), 'Curacao': (12.1696, 68.99), 'Aland': (60.1785, 19.9156)}

def train(dataset_dir, epochs=100):
    dataset = pathlib.Path(dataset_dir)
    train_ds = tf.keras.utils.image_dataset_from_directory(dataset, validation_split=0.1, subset="training", seed=1, image_size=(IMG_HEIGHT, IMG_WIDTH), batch_size=32)
    val_ds = tf.keras.utils.image_dataset_from_directory(dataset, validation_split=0.1, subset="validation", seed=1, image_size=(IMG_HEIGHT, IMG_WIDTH), batch_size=32)

    COUNTRIES = train_ds.class_names

    try:
        model = tf.keras.models.load_model(sys.path[0] + '/model')
    except:
        model = tf.keras.models.Sequential([
            tf.keras.layers.RandomFlip(mode='horizontal'),
            tf.keras.layers.RandomZoom(0.3),
            tf.keras.layers.RandomTranslation(0, 0.5),
            tf.keras.layers.Rescaling(1./255, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
            tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(128, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(256, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(512, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(512, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(len(COUNTRIES), activation = "softmax")
        ])

    model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])

    earlyStop = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=5)
    checkpointSave = tf.keras.callbacks.ModelCheckpoint(filepath=sys.path[0] + "/model", verbose=1)

    model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=[earlyStop, checkpointSave])

    return model


def predict(image_dir):
    model = tf.keras.models.load_model(sys.path[0] + '/model')
    image = tf.keras.utils.load_img(image_dir, target_size=(IMG_HEIGHT, IMG_WIDTH))

    image_array = tf.keras.utils.img_to_array(image)
    image_array = tf.expand_dims(image_array, 0)
    predictions = model.predict(image_array, verbose=0)

    confidence = tf.nn.softmax(predictions[0])
    prediction = COUNTRIES[np.argmax(confidence)]
    coordinates = COORDINATES[prediction]

    return prediction, coordinates, 100 * np.max(confidence)



if __name__ == '__main__':
    try:
        sys.argv[1]
    except:
        train("/Users/taharhidouani/Downloads/dataset/")
    else:
        prediction, coordinates, confidence = predict(sys.argv[1])
        print(prediction, coordinates, confidence)