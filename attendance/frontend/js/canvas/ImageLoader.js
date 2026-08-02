export default class ImageLoader {

    static load(url) {

        return new Promise((resolve, reject) => {

            const img = new Image();

            img.onload = () => resolve(img);

            img.onerror = reject;

            img.src = url;

        });

    }

}
