import React, { useState } from "react";
import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const Home = () => {
	const { store, dispatch } = useGlobalReducer();
	const [inputValueEmail, setInputValueEmail] = useState("");
	const [inputValuePassword, setInputValuePassword] = useState("");

	// Esto seria la pagina de register. Obviamente se tiene que trabajar
	async function sendToApi(e) {
		e.preventDefault();
		const response = await fetch("https://ideal-space-fortnight-x56rjqvx747fjqr-3001.app.github.dev/api/register", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({
				email: inputValueEmail,
				password: inputValuePassword
			})
		});

		const data = await response.json();
		console.log("Respuesta del servidor:", data);
	}

	return (
		<div className="text-center mt-5">
			<form onSubmit={sendToApi}>
				<input
					value={inputValueEmail}
					onChange={(e) => setInputValueEmail(e.target.value)}
					type="email"
					placeholder="Email"
				/>
				<input
					value={inputValuePassword}
					onChange={(e) => setInputValuePassword(e.target.value)}
					type="password"
					placeholder="Password"
				/>
				<button type="submit">Registrar</button>
			</form>
		</div>
	);
};
