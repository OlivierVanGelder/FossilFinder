function typeText(element, text, speed = 20) {
    element.textContent = '';
    return new Promise(resolve => {
        let i = 0;
        const timer = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
                resolve();
            }
        }, speed);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('preview');
    const analyzeBtn = document.getElementById('analyze-btn');
    const result = document.getElementById('result');
    const uploadBox = document.getElementById('upload-box');

    // Handle drag and drop
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('drag-over');
    });

    uploadBox.addEventListener('dragleave', () => {
        uploadBox.classList.remove('drag-over');
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('drag-over');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFile(file);
        }
    });

    // Handle click upload
    uploadBox.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

    function handleFile(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            analyzeBtn.style.display = 'inline-block';
            result.textContent = '';
            result.className = '';
        }
        reader.readAsDataURL(file);
    }

    const fossilInfo = {
        ammonite: {
            description: `Ammonites are an extinct group of marine mollusc animals. They were predatory, squid-like creatures that lived inside coiled shells. They first appeared around 400 million years ago and became extinct during the same event that killed the dinosaurs, 66 million years ago.
            
            Common locations: They can be found worldwide, with notable locations including:
            • Jurassic Coast, UK
            • Madagascar
            • Morocco
            
            Age: 400-66 million years ago (Devonian to Cretaceous periods)
            
            Fun fact: Their shells follow a perfect mathematical spiral!`,
            examples: [
                '/static/images/ammonite01.png',
                '/static/images/ammonite02.jpg',
                '/static/images/ammonite03.png'
            ]
        },
        belemnite: {
            description: `Belemnites were squid-like cephalopods that lived during the Mesozoic era. They had an internal shell called a guard or rostrum, which is the part most commonly found as a fossil. These bullet-shaped fossils were once thought to be "thunderbolts" fallen from the sky.
            
            Common locations:
            • European chalk deposits
            • North American marine deposits
            • Australian marine sediments
            
            Age: 240-65 million years ago (Triassic to Cretaceous periods)
            
            Fun fact: Their name comes from the Greek word "belemnon" meaning "dart" or "javelin"!`,
            examples: [
                '/static/images/belemnite01.jpg',
                '/static/images/belemnite02.png',
                '/static/images/belemnite03.png'
            ]
        },
        coral: {
            description: `Fossil corals are the preserved remains of ancient coral colonies. They provide important information about past climates and ocean conditions. Corals are actually animals that build limestone skeletons, which can become beautifully preserved as fossils.
            
            Common locations:
            • Ancient reef deposits worldwide
            • Limestone quarries
            • Mountain ranges that were once underwater
            
            Age: 485 million years ago to present
            
            Fun fact: Coral fossils can be so well preserved that individual polyp chambers are visible!`,
            examples: [
                '/static/images/coral01.png',
                '/static/images/coral02.png',
                '/static/images/coral03.png'
            ]
        },
        crinoid: {
            description: `Crinoids, also known as "sea lilies," are marine animals that have existed since the Ordovician period. Despite their plant-like appearance, they're actually animals related to starfish and sea urchins. Their fossils often appear as star-shaped segments or long stems.
            
            Common locations:
            • Limestone deposits worldwide
            • Midwestern United States
            • British Carboniferous rocks
            
            Age: 485 million years ago to present
            
            Fun fact: Modern crinoids still exist in today's oceans, earning them the title "living fossils"!`,
            examples: [
                '/static/images/crinoid01.png',
                '/static/images/crinoid02.png',
                '/static/images/crinoid03.png'
            ]
        },
        'leaf fossil': {
            description: `Leaf fossils provide crucial information about ancient climates and ecosystems. They can be preserved in several ways, including compression fossils where the original leaf material is preserved as a thin film, and impression fossils showing detailed vein patterns.
            
            Common locations:
            • Coal deposits
            • Lake bed sediments
            • River delta deposits
            
            Age: 360 million years ago to present (most common in Carboniferous to present)
            
            Fun fact: Scientists can determine ancient climate conditions by studying the size and shape of fossil leaves!`,
            examples: [
                '/static/images/leaf fossil01.png',
                '/static/images/leaf fossil02.png',
                '/static/images/leaf fossil03.png'
            ]
        },
        trilobite: {
            description: `Trilobites were marine arthropods that dominated the early Paleozoic seas. They were one of the most successful groups of animals, existing for over 270 million years. Trilobites could roll into balls for protection, similar to modern pill bugs.
            
            Common locations:
            • Morocco
            • Utah, USA
            • Czech Republic
            
            Age: 521-252 million years ago (Cambrian to Permian periods)
            
            Fun fact: Some trilobites had elaborate spines and could grow compound eyes with hundreds of lenses!`,
            examples: [
                '/static/images/trilobite01.jpg',
                '/static/images/trilobite02.png',
                '/static/images/trilobite03.png'
            ]
        }
    };

    analyzeBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) return;
    
        // Disable button and show loading state
        analyzeBtn.disabled = true;
        result.textContent = 'Analyzing...';
        result.className = 'loading';
        document.getElementById('fossil-info').style.display = 'none';
    
        // Clear previous images before new analysis
        const examplesDiv = document.querySelector('.fossil-examples');
        if (examplesDiv) {
            examplesDiv.innerHTML = ''; // Remove previous images
        }
    
        const formData = new FormData();
        formData.append('file', file);
    
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
    
            if (data.error) {
                await typeText(result, 'Error: ' + data.error);
                result.className = 'error';
            } else {
                const roundedConfidence = Math.round(data.confidence);
                await typeText(result, `Prediction: ${data.class} (Confidence: ${roundedConfidence}%)`);
                result.className = 'success';
    
                const fossilInfoDiv = document.getElementById('fossil-info');
                fossilInfoDiv.style.display = 'block';
    
                if (roundedConfidence >= 80 && fossilInfo[data.class.toLowerCase()]) {
                    const info = fossilInfo[data.class.toLowerCase()];
                    const descriptionDiv = fossilInfoDiv.querySelector('.fossil-description');
                    
                    descriptionDiv.innerHTML = '<div class="info-header">About ' + data.class + '</div>';
                    const descriptionP = document.createElement('p');
                    descriptionDiv.appendChild(descriptionP);
                    await typeText(descriptionP, info.description);
    
                    // Clear previous images again just in case
                    examplesDiv.innerHTML = ''; 
                    
                    examplesDiv.innerHTML = `
                        <div class="info-header">Example Images</div>
                        ${info.examples.map(img => `
                            <img src="${img}" alt="${data.class} example" class="example-image">
                        `).join('')}
                    `;
                } else {
                    fossilInfoDiv.innerHTML = '<div class="fossil-description"></div>';
                    const lowConfDiv = fossilInfoDiv.querySelector('.fossil-description');
    
                    const header = document.createElement('div');
                    header.className = 'info-header';
                    lowConfDiv.appendChild(header);
                    await typeText(header, 'Low Confidence Prediction');
    
                    const p1 = document.createElement('p');
                    lowConfDiv.appendChild(p1);
                    await typeText(p1, 'Sorry, we do not feel confident enough to identify this fossil accurately.');
    
                    const p2 = document.createElement('p');
                    lowConfDiv.appendChild(p2);
                    await typeText(p2, 'This could be due to several reasons:');
    
                    const ul1 = document.createElement('ul');
                    lowConfDiv.appendChild(ul1);
                    const reasons = [
                        'The fossil might be of a type not yet known to our AI',
                        'The image might lack sufficient contrast or clarity',
                        'The lighting or angle of the photograph might not be optimal'
                    ];
                    for (const reason of reasons) {
                        const li = document.createElement('li');
                        ul1.appendChild(li);
                        await typeText(li, reason);
                    }
    
                    const p3 = document.createElement('p');
                    lowConfDiv.appendChild(p3);
                    await typeText(p3, 'We are continuously improving our AI for a better user experience. Please try another picture, ensuring:');
    
                    const ul2 = document.createElement('ul');
                    lowConfDiv.appendChild(ul2);
                    const tips = [
                        'Good lighting conditions',
                        'Clear focus on the fossil',
                        'High contrast between the fossil and background'
                    ];
                    for (const tip of tips) {
                        const li = document.createElement('li');
                        ul2.appendChild(li);
                        await typeText(li, tip);
                    }
                }
            }
        } catch (error) {
            await typeText(result, 'Error: ' + error.message);
            result.className = 'error';
        } finally {
            analyzeBtn.disabled = false;
        }
    });    
});