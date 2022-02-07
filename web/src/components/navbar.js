function NavBar() {
	return (
		<div
			className="column is-2 is-flex is-flex-direction-column is-align-items-center has-background-dark has-text-light"
		>
			<div className="is-size-3 mt-4">
				Debate It
			</div>
			<div className="my-6">
				ALPACAMAX
			</div>
			{["Yours", "Topics", "Debates"].map((text, index) => (
				<div className="py-4 button is-dark is-fullwidth">
					{text}
				</div>
			))}
		</div>
	);
};

export default NavBar;