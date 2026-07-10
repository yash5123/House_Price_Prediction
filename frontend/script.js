// Frontend logic for House Price Estimator
(() => {
    'use strict';

    // Configuration
    // When served from FastAPI, the API is on the same origin.
    // When opened as a standalone file, fall back to localhost.
    const API_BASE = window.location.origin.includes('file://') 
        ? 'http://127.0.0.1:8000' 
        : window.location.origin;

    // DOM Elements
    const form = document.getElementById('prediction-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');

    const resultEmpty = document.getElementById('result-empty');
    const resultLoading = document.getElementById('result-loading');
    const resultSuccess = document.getElementById('result-success');
    const resultError = document.getElementById('result-error');

    const priceValue = document.getElementById('price-value');
    const confidenceBadge = document.getElementById('confidence-badge');
    const confidenceText = document.getElementById('confidence-text');
    const errorDesc = document.getElementById('error-desc');

    const btnReset = document.getElementById('btn-reset');
    const btnRetry = document.getElementById('btn-retry');

    // Field definitions
    const fields = [
        { id: 'area_income', label: 'Average Area Income', min: 0, max: 500000 },
        { id: 'area_house_age', label: 'Average House Age', min: 0, max: 100 },
        { id: 'area_no_of_rooms', label: 'Average Number of Rooms', min: 1, max: 30 },
        { id: 'area_no_of_bedrooms', label: 'Average Number of Bedrooms', min: 0, max: 20 },
        { id: 'area_population', label: 'Area Population', min: 0, max: 200000 },
    ];

    // State Management
    function showState(state) {
        [resultEmpty, resultLoading, resultSuccess, resultError].forEach(el => {
            el.classList.add('hidden');
        });

        switch (state) {
            case 'empty':
                resultEmpty.classList.remove('hidden');
                break;
            case 'loading':
                resultLoading.classList.remove('hidden');
                break;
            case 'success':
                resultSuccess.classList.remove('hidden');
                break;
            case 'error':
                resultError.classList.remove('hidden');
                break;
        }
    }

    function setSubmitLoading(isLoading) {
        submitBtn.disabled = isLoading;
        btnText.textContent = isLoading ? 'Estimating...' : 'Estimate Price';
    }

    // Validation
    function validateField(field) {
        const input = document.getElementById(field.id);
        const wrapper = input.closest('.input-wrapper');
        const helpEl = document.getElementById(`${field.id}_help`);
        const value = input.value.trim();

        // Remove existing error styling
        wrapper.classList.remove('input-error');
        
        // Remove existing error message
        const existingError = wrapper.parentElement.querySelector('.form-error-msg');
        if (existingError) existingError.remove();

        // Restore help text
        if (helpEl) helpEl.style.display = '';

        if (value === '') {
            showFieldError(wrapper, helpEl, `${field.label} is required`);
            return false;
        }

        const num = parseFloat(value);
        if (isNaN(num)) {
            showFieldError(wrapper, helpEl, `Please enter a valid number`);
            return false;
        }

        if (num < field.min || num > field.max) {
            showFieldError(wrapper, helpEl, `Must be between ${field.min.toLocaleString()} and ${field.max.toLocaleString()}`);
            return false;
        }

        return true;
    }

    function showFieldError(wrapper, helpEl, message) {
        wrapper.classList.add('input-error');
        if (helpEl) helpEl.style.display = 'none';

        const errorMsg = document.createElement('span');
        errorMsg.className = 'form-error-msg';
        errorMsg.textContent = message;
        wrapper.parentElement.appendChild(errorMsg);
    }

    function validateAll() {
        let isValid = true;
        for (const field of fields) {
            if (!validateField(field)) {
                isValid = false;
            }
        }
        return isValid;
    }

    // Clear validation errors on input
    fields.forEach(field => {
        const input = document.getElementById(field.id);
        input.addEventListener('input', () => {
            const wrapper = input.closest('.input-wrapper');
            const helpEl = document.getElementById(`${field.id}_help`);
            wrapper.classList.remove('input-error');
            const existingError = wrapper.parentElement.querySelector('.form-error-msg');
            if (existingError) existingError.remove();
            if (helpEl) helpEl.style.display = '';
        });
    });

    // Animated Price Counter
    function animatePrice(targetPrice) {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (prefersReducedMotion) {
            priceValue.textContent = formatNumber(Math.round(targetPrice));
            return;
        }

        const duration = 1200; // ms
        const startTime = performance.now();
        const startValue = 0;

        function easeOutCubic(t) {
            return 1 - Math.pow(1 - t, 3);
        }

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedProgress = easeOutCubic(progress);
            const currentValue = Math.round(startValue + (targetPrice - startValue) * easedProgress);

            priceValue.textContent = formatNumber(currentValue);

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    function formatNumber(num) {
        return num.toLocaleString('en-US');
    }

    // API Call
    async function predictPrice(data) {
        const response = await fetch(`${API_BASE}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorBody = await response.json().catch(() => null);

            if (response.status === 422 && errorBody?.detail) {
                // Pydantic validation error: make it human-readable
                const messages = errorBody.detail.map(err => {
                    const field = err.loc?.[1] || 'input';
                    const friendlyField = field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                    return `${friendlyField}: ${err.msg}`;
                });
                throw new Error(messages.join('. '));
            }

            throw new Error(
                errorBody?.detail || 
                errorBody?.error || 
                `Server returned ${response.status}. Please try again.`
            );
        }

        return response.json();
    }

    // Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Client-side validation
        if (!validateAll()) return;

        // Gather data
        const data = {};
        fields.forEach(field => {
            data[field.id] = parseFloat(document.getElementById(field.id).value);
        });

        // Show loading
        setSubmitLoading(true);
        showState('loading');

        try {
            const result = await predictPrice(data);

            // Show success
            showState('success');

            // Animate the price
            animatePrice(Math.round(result.predicted_price));

            // Set confidence badge
            const confidenceStr = result.confidence || 'Unknown';
            confidenceText.textContent = confidenceStr;

            // Style confidence badge
            confidenceBadge.classList.remove('moderate', 'low');
            if (confidenceStr.toLowerCase().includes('moderate')) {
                confidenceBadge.classList.add('moderate');
            } else if (confidenceStr.toLowerCase().includes('low')) {
                confidenceBadge.classList.add('low');
            }

        } catch (err) {
            showState('error');
            errorDesc.textContent = err.message || 'We could not process your request. Please check your inputs and try again.';
        } finally {
            setSubmitLoading(false);
        }
    });

    // Reset / Retry
    btnReset.addEventListener('click', () => {
        showState('empty');
        form.reset();
        // Scroll form into view on mobile
        if (window.innerWidth <= 768) {
            form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });

    btnRetry.addEventListener('click', () => {
        showState('empty');
        // Scroll form into view on mobile
        if (window.innerWidth <= 768) {
            form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });

    // Header Scroll Dynamics
    const header = document.querySelector('.site-header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 20) {
                header.classList.add('header-scrolled');
            } else {
                header.classList.remove('header-scrolled');
            }
        });
    }

    // Interactive SVG Chart Tooltips
    const points = document.querySelectorAll('.chart-point');
    const tooltip = document.getElementById('chart-tooltip');
    const chartContainer = document.querySelector('.chart-container');

    if (points.length && tooltip && chartContainer) {
        points.forEach(point => {
            point.addEventListener('mouseenter', () => {
                const income = point.getAttribute('data-income');
                const price = point.getAttribute('data-price');
                tooltip.innerHTML = `<strong>Income:</strong> ${income}<br><strong>Value:</strong> ${price}`;
                tooltip.classList.remove('hidden');
            });

            point.addEventListener('mousemove', (e) => {
                const rect = chartContainer.getBoundingClientRect();
                const x = e.clientX - rect.left + 15;
                const y = e.clientY - rect.top - 55;
                tooltip.style.left = `${x}px`;
                tooltip.style.top = `${y}px`;
            });

            point.addEventListener('mouseleave', () => {
                tooltip.classList.add('hidden');
            });
        });
    }

})();
