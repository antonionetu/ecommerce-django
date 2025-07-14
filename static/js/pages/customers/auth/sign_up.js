document.addEventListener('DOMContentLoaded', function () {
	const hiddenInput = document.getElementById('cart_reference');
	hiddenInput.value = cartReference;

	const steps = document.querySelectorAll('.form-step');
	let currentStep = 0;

	const showStep = (index) => {
		steps.forEach((step, i) => {
			step.classList.toggle('active', i === index);
		});
	};

	const nextStep = () => {
		if (currentStep < steps.length - 1) {
			currentStep++;
			showStep(currentStep);
		}
	};

	const prevStep = () => {
		if (currentStep > 0) {
			currentStep--;
			showStep(currentStep);
		}
	};

	document.getElementById('next-1').addEventListener('click', () => {
		nextStep();
	});

	document.getElementById('next-2').addEventListener('click', () => {
		nextStep();
	});

	document.getElementById('prev-2').addEventListener('click', () => {
		prevStep();
	});

	document.getElementById('prev-3').addEventListener('click', () => {
		prevStep();
	});

	showStep(currentStep);

	document.getElementById('multi-step-form').addEventListener('keydown', (e) => {
		if (e.key === 'Enter') {
			e.preventDefault();
			currentStep < steps.length - 1
				? nextStep()
				: document.getElementById('multi-step-form').submit()
		}
	});

	const cepInput = document.getElementById('id_postal_code');
	cepInput.addEventListener('blur', () => {
		const cep = cepInput.value.replace(/\D/g, '');

		if (cep.length !== 8) return;

		fetch(`https://viacep.com.br/ws/${cep}/json/`)
			.then(response => response.json())
			.then(data => {
				document.getElementById('id_street').value = data.logradouro || '';
				document.getElementById('id_neighborhood').value = data.bairro || '';
				document.getElementById('id_city').value = data.localidade || '';
				document.getElementById('id_state').value = data.uf || '';
				document.getElementById('id_country').value = 'Brasil';
			})
			.catch(() => {
				alert('Erro ao buscar o CEP. Tente novamente.');
			});
	});
});
