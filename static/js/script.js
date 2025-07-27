// Air Quality Prediction Website JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializePredictionForm();
    initializeCharts();
    initializeForestAnimation();
    initializeSmoothScrolling();
    initializeAnimations();
});

// Prediction Form Handling
function initializePredictionForm() {
    const form = document.getElementById('predictionForm');
    const resultDiv = document.getElementById('predictionResult');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="loading"></span> Predicting...';
            submitBtn.disabled = true;
            
            try {
                // Collect form data
                const formData = new FormData(form);
                const data = {};
                
                for (let [key, value] of formData.entries()) {
                    data[key] = value;
                }
                
                // Send prediction request
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    displayPredictionResult(result.prediction, result.message);
                } else {
                    displayError(result.message);
                }
                
            } catch (error) {
                displayError('An error occurred while making the prediction.');
                console.error('Prediction error:', error);
            } finally {
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        });
    }
}

// Display Prediction Result
function displayPredictionResult(prediction, message) {
    const resultDiv = document.getElementById('predictionResult');
    const predictionValue = document.getElementById('predictionValue');
    const predictionMessage = document.getElementById('predictionMessage');
    const airQualityStatus = document.getElementById('airQualityStatus');
    
    // Set prediction value
    predictionValue.textContent = `${prediction} μg/m³`;
    
    // Set message
    predictionMessage.textContent = message;
    
    // Determine air quality status and color
    let status, statusClass;
    if (prediction <= 12) {
        status = 'Good';
        statusClass = 'bg-success';
    } else if (prediction <= 35.4) {
        status = 'Moderate';
        statusClass = 'bg-warning';
    } else if (prediction <= 55.4) {
        status = 'Unhealthy for Sensitive Groups';
        statusClass = 'bg-orange';
    } else if (prediction <= 150.4) {
        status = 'Unhealthy';
        statusClass = 'bg-danger';
    } else if (prediction <= 250.4) {
        status = 'Very Unhealthy';
        statusClass = 'bg-purple';
    } else {
        status = 'Hazardous';
        statusClass = 'bg-dark';
    }
    
    airQualityStatus.textContent = status;
    airQualityStatus.className = `badge ${statusClass} fs-6 p-3 mt-3`;
    
    // Show result with animation
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Display Error
function displayError(message) {
    const resultDiv = document.getElementById('predictionResult');
    const predictionValue = document.getElementById('predictionValue');
    const predictionMessage = document.getElementById('predictionMessage');
    const airQualityStatus = document.getElementById('airQualityStatus');
    
    predictionValue.textContent = 'Error';
    predictionValue.className = 'display-4 fw-bold text-danger';
    predictionMessage.textContent = message;
    airQualityStatus.style.display = 'none';
    
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Initialize Charts
function initializeCharts() {
    // Feature Importance Chart
    const featureChart = document.getElementById('featureImportanceChart');
    if (featureChart) {
        const ctx = featureChart.getContext('2d');
        
        // Sample feature importance data (replace with actual data from backend)
        const featureData = {
            labels: ['PM2.5 Lag', 'Temperature', 'Dew Point', 'Pressure', 'Wind Speed', 'Hour', 'Month', 'Snow Hours', 'Rain Hours', 'Wind Direction'],
            datasets: [{
                label: 'Feature Importance',
                data: [0.245, 0.189, 0.156, 0.134, 0.123, 0.098, 0.087, 0.045, 0.032, 0.025],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(199, 199, 199, 0.8)',
                    'rgba(83, 102, 255, 0.8)',
                    'rgba(78, 252, 3, 0.8)',
                    'rgba(252, 3, 244, 0.8)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(199, 199, 199, 1)',
                    'rgba(83, 102, 255, 1)',
                    'rgba(78, 252, 3, 1)',
                    'rgba(252, 3, 244, 1)'
                ],
                borderWidth: 2
            }]
        };
        
        new Chart(ctx, {
            type: 'bar',
            data: featureData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Feature Importance in Random Forest Model'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Importance Score'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Features'
                        }
                    }
                }
            }
        });
    }
}

// Forest Animation
function initializeForestAnimation() {
    const canvas = document.getElementById('forestCanvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        const trees = [];
        
        // Create trees
        for (let i = 0; i < 8; i++) {
            trees.push({
                x: 50 + i * 45,
                y: 250,
                height: 60 + Math.random() * 40,
                width: 20 + Math.random() * 15,
                color: `hsl(${120 + Math.random() * 40}, 70%, 40%)`
            });
        }
        
        function drawTree(tree) {
            // Draw trunk
            ctx.fillStyle = '#8B4513';
            ctx.fillRect(tree.x - tree.width/4, tree.y - tree.height/3, tree.width/2, tree.height/3);
            
            // Draw leaves
            ctx.fillStyle = tree.color;
            ctx.beginPath();
            ctx.arc(tree.x, tree.y - tree.height/2, tree.width, 0, Math.PI * 2);
            ctx.fill();
            
            // Draw smaller leaves on top
            ctx.fillStyle = `hsl(${120 + Math.random() * 40}, 80%, 50%)`;
            ctx.beginPath();
            ctx.arc(tree.x, tree.y - tree.height/1.5, tree.width * 0.7, 0, Math.PI * 2);
            ctx.fill();
        }
        
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw ground
            ctx.fillStyle = '#90EE90';
            ctx.fillRect(0, 250, canvas.width, 50);
            
            // Draw trees
            trees.forEach(tree => {
                drawTree(tree);
            });
            
            // Add some floating particles (representing data points)
            if (Math.random() < 0.1) {
                const particle = {
                    x: Math.random() * canvas.width,
                    y: 0,
                    speed: 1 + Math.random() * 2,
                    size: 2 + Math.random() * 3,
                    color: `hsl(${200 + Math.random() * 60}, 70%, 60%)`
                };
                
                function animateParticle() {
                    ctx.fillStyle = particle.color;
                    ctx.beginPath();
                    ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                    ctx.fill();
                    
                    particle.y += particle.speed;
                    
                    if (particle.y < canvas.height) {
                        requestAnimationFrame(animateParticle);
                    }
                }
                
                animateParticle();
            }
            
            requestAnimationFrame(animate);
        }
        
        animate();
    }
}

// Smooth Scrolling
function initializeSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update active nav link
                document.querySelectorAll('.nav-link').forEach(navLink => {
                    navLink.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });
}

// Initialize Animations
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animateElements = document.querySelectorAll('.card, .feature-item, .metric-circle');
    animateElements.forEach(el => {
        observer.observe(el);
    });
    
    // Add CSS for animation
    const style = document.createElement('style');
    style.textContent = `
        .card, .feature-item, .metric-circle {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .animate-in {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    document.head.appendChild(style);
}

// Form Validation
function validateForm() {
    const inputs = document.querySelectorAll('#predictionForm input, #predictionForm select');
    let isValid = true;
    
    inputs.forEach(input => {
        if (input.hasAttribute('required') && !input.value) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });
    
    return isValid;
}

// Add form validation listeners
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('#predictionForm input, #predictionForm select');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                this.classList.remove('is-invalid');
            }
        });
    });
});

// Utility Functions
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add some sample data for demonstration
function populateSampleData() {
    // Generate random but reasonable values for each field
    const cbwdOptions = ['NW', 'NE', 'SE', 'SW', 'cv'];
    const sampleData = {
        'DEWP': Math.floor(Math.random() * 40) - 20, // -20 to 19
        'TEMP': Math.floor(Math.random() * 40) - 10, // -10 to 29
        'PRES': Math.floor(Math.random() * 40) + 980, // 980 to 1019
        'Iws': (Math.random() * 40).toFixed(2), // 0 to 40
        'Is': Math.random() < 0.1 ? 1 : 0, // 0 or 1, mostly 0
        'Ir': Math.random() < 0.1 ? 1 : 0, // 0 or 1, mostly 0
        'cbwd': cbwdOptions[Math.floor(Math.random() * cbwdOptions.length)],
        'hour': Math.floor(Math.random() * 24), // 0 to 23
        'month': Math.floor(Math.random() * 12) + 1, // 1 to 12
        'pm2_5_lag1': (Math.random() * 300).toFixed(1) // 0 to 300
    };
    Object.keys(sampleData).forEach(key => {
        const input = document.getElementById(key);
        if (input) {
            input.value = sampleData[key];
        }
    });
}

// Add sample data button functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add a button to populate sample data (for demonstration)
    const form = document.getElementById('predictionForm');
    if (form) {
        const sampleBtn = document.createElement('button');
        sampleBtn.type = 'button';
        sampleBtn.className = 'btn btn-outline-secondary btn-sm ms-2';
        sampleBtn.innerHTML = '<i class="fas fa-magic me-1"></i>Sample Data';
        sampleBtn.onclick = populateSampleData;
        
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.parentNode.appendChild(sampleBtn);
    }
}); 