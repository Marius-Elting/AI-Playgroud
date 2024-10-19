"use client";
import React, { useState } from 'react';
import styles from './page.module.scss';

const ImageFetcher: React.FC = () => {
    const [inputValue, setInputValue] = useState<string>('');
    const [imageUrl, setImageUrl] = useState<string | null>(null);

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setInputValue(event.target.value);
    };

    const fetchImage = async () => {
        try {
            const formData = new FormData();
            formData.append('prompt', inputValue);
            const response = await fetch("http://localhost:8000/api/chat/generate_image", {
                method: 'POST',
                body: formData,
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json()
            console.log(data)
            setImageUrl(data.image);
        } catch (error) {
            console.error('Error fetching the image:', error);
        }
    };

    return (
        <div className={styles.imageFetcher}>
            <input
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                placeholder="Enter image URL"
                className={styles.inputField}
            />
            <button onClick={fetchImage} className={styles.fetchButton}>
                Fetch Image
            </button>
            {imageUrl && (
                <img src={imageUrl} alt="Fetched" className={styles.fetchedImage} />
            )}
        </div>
    );
};

export default ImageFetcher;