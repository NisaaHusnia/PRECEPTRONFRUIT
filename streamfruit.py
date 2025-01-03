import pickle
import streamlit as st
import pandas as pd

# Fungsi untuk memuat model dari file pickle
def load_model(model_path):
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        st.error(f"Error memuat model: {e}")
        return None

# Konfigurasi halaman Streamlit dengan tampilan terang
st.set_page_config(page_title="Fruit Prediction", page_icon="🍎", layout="wide")

# Header dan Deskripsi dengan styling
st.markdown("""
    <style>
        .title {
            font-size: 48px;
            color: #4CAF50;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }
        .description {
            font-size: 18px;
            color: #333;
            margin-top: 10px;
            text-align: center;
        }
        .header-text {
            font-size: 24px;
            color: #FF6347;
            text-align: center;
            font-weight: bold;
            margin-top: 20px;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            font-size: 18px;
            cursor: pointer;
            border-radius: 5px;
        }
        .button:hover {
            background-color: #45a049;
        }
        .success-text {
            font-size: 24px;
            color: #4CAF50;
            font-weight: bold;
        }
        .container-box {
            border: 2px solid #4CAF50;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            background-color: #f9f9f9;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="title">🎯 Fruit Prediction Model</p>', unsafe_allow_html=True)

# Deskripsi aplikasi
st.markdown('<p class="description"> fitur untuk memprediksi jenis buah.</p>', unsafe_allow_html=True)

# Dataset untuk prediksi
dataset = {
    "Fruit Dataset": {
        "model": "perceptronfruit.pkl",  # Menggunakan nama model yang baru
        "sample_data": "fruit.xlsx",
        "input_columns": ["diameter", "weight", "red", "green", "blue"],
        "species_labels": ['grapefruit', 'orange']
    }
}

# Memilih dataset
dataset_choice = "Fruit Dataset"  # Kita hanya menggunakan dataset buah
selected_dataset = dataset[dataset_choice]
model_path = selected_dataset["model"]
sample_data_path = selected_dataset["sample_data"]
input_columns = selected_dataset["input_columns"]
species_labels = selected_dataset["species_labels"]

# Memulai container
with st.container():
    # Menampilkan Model yang Dipilih dan Memuat Model
    st.write(f"**Model yang dipilih:** {model_path}")
    model = load_model(model_path)

    if model is not None:
        st.success("✔️ Model berhasil dimuat!")

        # Memuat data sampel untuk prediksi
        st.markdown('<p class="header-text">Contoh data untuk prediksi:</p>', unsafe_allow_html=True)
        if sample_data_path.endswith('.xlsx'):
            sample_data = pd.read_excel(sample_data_path)
        else:
            st.error("Format file data tidak didukung.")
            sample_data = pd.DataFrame()  # Set data kosong jika format tidak dikenal

        # Menampilkan data sampel dalam kotak
        with st.expander("Klik untuk melihat contoh data"):
            st.dataframe(sample_data, width=800)

        # Input untuk prediksi
        st.markdown('<p class="header-text">Masukkan data untuk prediksi:</p>', unsafe_allow_html=True)
        input_data = {}

        for col in input_columns:
            input_data[col] = st.number_input(f"Masukkan nilai untuk **{col}**", value=sample_data[col].iloc[0] if col in sample_data else 0.0)

        # Sinkronkan kolom input dengan kolom yang digunakan oleh model
        data_for_prediction = pd.DataFrame([input_data], columns=input_columns)

        # Tombol untuk memulai prediksi
        st.markdown("---")
        if st.button("🔮 **Prediksi**", key="predict_button"):
            if not data_for_prediction.empty:
                try:
                    prediction = model.predict(data_for_prediction)
                    
                    # Menampilkan hasil prediksi dengan nama spesies untuk Fruit Dataset
                    predicted_species = species_labels[prediction[0]]  # Ambil label berdasarkan hasil prediksi
                    st.markdown(f"<p class='success-text'>**Hasil Prediksi untuk {dataset_choice}:** {predicted_species} (species {prediction[0]})</p>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Terjadi kesalahan dalam prediksi: {e}")
            else:
                st.error("Data untuk prediksi kosong!")
    else:
        st.error("Model gagal dimuat.")
