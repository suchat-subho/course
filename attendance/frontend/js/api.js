/******************************************************************************
 * api.js
 *
 * Handles loading of:
 *  - manifest.json
 *  - progress.json
 *
 * Provides helper functions for all pages.
 ******************************************************************************/
import { state } from "./state.js";
const DATASET = "dataset/RawPicture";

const MANIFEST_FILE = `${DATASET}/manifest.json`;
const PROGRESS_FILE = `${DATASET}/progress.json`;

let manifest = [];
let progress = {};

async function loadJSON(url)
{
    const response = await fetch(url);

    if (!response.ok)
    {
        throw new Error(`Unable to load ${url}`);
    }

    return await response.json();
}

export async function initialize()
{
    const manifestData = await loadJSON(MANIFEST_FILE);
    const progressData = await loadJSON(PROGRESS_FILE);

    manifest = manifestData.images;
    progress = progressData;

    state.manifest = manifest;
    state.progress = progress;
    state.images = getMergedData();
}
export function getImages()
{
    return manifest;
}

export function getProgress()
{
    return progress;
}

export function getImage(index)
{
    return manifest[index];
}

export function getImageCount()
{
    return manifest.length;
}

export function getImageURL(filename)
{
    return `${DATASET}/${filename}`;
}

export function getStatus(filename)
{
    return progress[filename] || null;
}

export function getMergedData()
{
    return manifest.map(image => {

        return {

            ...image,

            ...(progress[image.filename] || {})

        };

    });
}

export function getPendingImages()
{
    return getMergedData().filter(
        item => item.status === "Pending"
    );
}

export function getCompletedImages()
{
    return getMergedData().filter(
        item => item.status === "Completed"
    );
}

export function getClasses()
{
    return [...new Set(manifest.map(i => i.class))];
}

export function getDates()
{
    return [...new Set(manifest.map(i => i.date))];
}

export function findImage(filename)
{
    return manifest.find(
        image => image.filename === filename
    );
}
