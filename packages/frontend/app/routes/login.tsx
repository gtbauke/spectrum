import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Logo } from "~/components/ui/brand/logo.component";
import { Button } from "~/components/ui/buttons/button.component";
import { Field } from "~/components/ui/forms/field/field.component";
import { PasswordToggle } from "~/components/ui/forms/input/password-toggle.component";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { RedirectLink } from "~/components/ui/redirects/redirect-link.component";
import { useLoginMutation } from "~/hooks/use-login.hook";
import { loginCredentialsSchema } from "~/schemas/dtos/auth.dto";

export default function Login() {
	const [showPassword, setShowPassword] = useState(false);
	const { mutate, isPending, error } = useLoginMutation();
	const {
		formState: { errors, isValid },
		register,
		handleSubmit,
	} = useForm({
		defaultValues: {
			email: "",
			password: "",
		},
		resolver: zodResolver(loginCredentialsSchema),
	});

	const onSubmit = handleSubmit((data) => {
		mutate(data);
	});

	return (
		<div className="flex h-screen w-full bg-background text-white">
			<div className="hidden lg:flex flex-1 relative flex-col justify-between p-10 bg-[radial-gradient(#2D3343_1px,transparent_1px)] bg-size-[40px_40px]">
				<div className="z-10">
					<Logo />
					<p className="mt-2 text-gray-400 max-w-sm">
						Explore, visualize, and derive insights from your data with Symbolic
						Regression.
					</p>
				</div>

				<div className="absolute inset-0 flex items-center justify-center overflow-hidden opacity-30">
					<div className="w-125 h-125 border border-violet-500/20 rounded-full animate-pulse blur-3xl" />
				</div>

				<div className="z-10 text-xs text-gray-600">
					© 2026 Gustavo Teodoro Bauke
				</div>
			</div>

			<div className="w-full lg:w-120 flex flex-col justify-center p-8 md:p-16 bg-background-surface border-l border-border">
				<div className="w-full max-w-sm mx-auto space-y-10">
					{error && (
						<div className="p-3 text-red-400 bg-red-500/10 rounded">
							{error.message}
						</div>
					)}

					<div className="space-y-2">
						<h2 className="text-3xl font-bold">Welcome back</h2>
						<p className="text-gray-400 text-sm">
							Enter your credentials to access your workspace.
						</p>
					</div>

					<form className="space-y-6" onSubmit={onSubmit}>
						<Field error={errors.email}>
							<Field.Label>Email</Field.Label>
							<Field.Control>
								<TextInput
									type="email"
									placeholder="name@company.com"
									{...register("email")}
								/>
							</Field.Control>
							<Field.Error />
						</Field>

						<Field error={errors.password}>
							<Field.Header>
								<Field.Label>Password</Field.Label>
								<Field.Action to="/password-reset">Forgot?</Field.Action>
							</Field.Header>
							<Field.Control>
								<TextInput
									type={showPassword ? "text" : "password"}
									placeholder="••••••••"
									{...register("password")}
								/>
								<Field.Slot side="right">
									<PasswordToggle
										visible={showPassword}
										onToggle={() => setShowPassword((p) => !p)}
									/>
								</Field.Slot>
							</Field.Control>
							<Field.Error />
						</Field>

						<Button
							type="submit"
							disabled={isPending || !isValid}
							isLoading={isPending}
						>
							Sign In
						</Button>
					</form>

					<div className="mt-8 pt-8 border-t border-border flex justify-center space-x-4">
						<RedirectLink
							to="/signup"
							className="text-xs text-gray-500 hover:text-white transition cursor-pointer"
						>
							Create Account
						</RedirectLink>
					</div>
				</div>
			</div>
		</div>
	);
}
