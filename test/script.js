const button = document.getElementById('mode-toggle');

button.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
});




const text = "Moritz Staat, Web Developer, Gründer, Innovator";
let index = 0;

function typeWriter() {
    if (index < text.length) {
        document.getElementById("typed-text").innerHTML += text.charAt(index);
        index++;
        setTimeout(typeWriter, 100);
    }
}

window.onload = typeWriter;






let currentIndex = 0;
const testimonials = document.querySelectorAll('.testimonial');

function showTestimonial(index) {
    testimonials.forEach((testimonial, i) => {
        testimonial.style.display = (i === index) ? 'block' : 'none';
    });
}

function nextTestimonial() {
    currentIndex = (currentIndex + 1) % testimonials.length;
    showTestimonial(currentIndex);
}

setInterval(nextTestimonial, 3000);