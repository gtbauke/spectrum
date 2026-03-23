import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Logo } from "~/components/ui/brand/logo.component";
import { Button } from "~/components/ui/buttons/button.component";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { RedirectLink } from "~/components/ui/redirects/redirect-link.component";
import { useSignupMutation } from "~/hooks/use-signup.hook";
import { signupDtoSchema } from "~/schemas/dtos/auth.dto";

export default function SignUp() {
	const { mutate, isPending, error } = useSignupMutation();
	const {
		register,
		handleSubmit,
		formState: { errors, isValid },
	} = useForm({
		resolver: zodResolver(signupDtoSchema),
	});

	const onSubmit = handleSubmit((data) => mutate(data));

	return (
		<div className="flex h-screen w-full bg-background text-white">
			<div className="hidden lg:flex flex-1 flex-col justify-between p-10 bg-[#111319] border-r border-border relative overflow-hidden">
				<div className="z-10 space-y-20">
					<Logo />

					<div className="space-y-6">
						<h2 className="text-4xl font-bold leading-tight">
							Build, Scale, and <br />
							<span className="text-primary-600 underline decoration-primary-500/30 underline-offset-8">
								Regress.
							</span>
						</h2>

						<p className="text-gray-400 text-lg max-w-sm">
							Join the next generation of symbolic regression practitioners.
							Manage datasets and profiles in one unified IDE.
						</p>
					</div>
				</div>

				<div className="absolute bottom-[-10%] left-[-10%] w-125 h-125 bg-violet-600/10 blur-[120px] rounded-full" />
			</div>

			<div className="w-full lg:w-137.5 overflow-y-auto bg-background-surface p-8 md:p-16">
				<div className="max-w-sm mx-auto space-y-6">
					{error && (
						<div className="p-3 text-red-400 bg-red-500/10 rounded">
							{error.message}
						</div>
					)}

					<header>
						<h2 className="text-2xl font-bold">Create your account</h2>
						<p className="text-gray-500 text-sm">
							Already have an account?{" "}
							<RedirectLink to="/login">Log in</RedirectLink>
						</p>
					</header>

					<form onSubmit={onSubmit} className="space-y-6">
						<div className="grid grid-cols-2 gap-4">
							<TextInput
								label="First Name"
								placeholder="John"
								{...register("first_name")}
								error={errors.first_name}
							/>
							<TextInput
								label="Last Name"
								placeholder="Doe"
								{...register("last_name")}
								error={errors.last_name}
							/>
						</div>

						<TextInput
							label="Email Address"
							type="email"
							placeholder="john@company.com"
							{...register("email")}
							error={errors.email}
						/>

						<TextInput
							label="Password"
							type="password"
							placeholder="Create a strong password"
							{...register("password")}
							error={errors.password}
						/>

						<Button
							type="submit"
							disabled={isPending || !isValid}
							isLoading={isPending}
						>
							Create Account
						</Button>
					</form>
				</div>
			</div>
		</div>
	);
}
