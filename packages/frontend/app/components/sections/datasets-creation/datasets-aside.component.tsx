import { zodResolver } from "@hookform/resolvers/zod";
import { useCallback } from "react";
import { type SubmitHandler, useForm } from "react-hook-form";
import { useNavigate } from "react-router";
import { FormInput } from "~/components/ui/forms/form-input.component";
import { FormTextArea } from "~/components/ui/forms/form-textarea.component";
import { useDatasetCreationContext } from "~/contexts/dataset-creation.context";
import {
    type CreateDatasetData,
    createDatasetValidator,
} from "~s/datasets.validator";

// TODO: handle API call
export function DatasetsAsideSection() {
    const { file } = useDatasetCreationContext();
    const navigate = useNavigate();

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<CreateDatasetData>({
        defaultValues: {
            title: file?.originalName || "",
            description: "",
        },
        resolver: zodResolver(createDatasetValidator),
    });

    const onCancel = useCallback(() => {
        reset();
        navigate("/");
    }, [reset, navigate]);

    const onSubmit: SubmitHandler<CreateDatasetData> = (data) => {
        console.log(errors);
        console.log(data);
    };

    return (
        <div className="h-full bg-gray-900 p-4 space-y-8">
            <h2 className="text-xl font-bold">Configure your dataset</h2>

            <form
                className="flex flex-col gap-3"
                onSubmit={handleSubmit(onSubmit)}
                onReset={onCancel}
            >
                <FormInput
                    label="Dataset name"
                    error={errors.title}
                    required
                    {...register("title", { required: true })}
                />

                <FormTextArea
                    label="Dataset description"
                    className="min-h-30"
                    error={errors.description}
                    {...register("description")}
                />

                <div className="flex flex-col gap-2">
                    <input
                        type="submit"
                        value="Continue"
                        className="cursor-pointer p-2 bg-green-600 hover:bg-green-700 active:bg-green-800 rounded-sm font-bold"
                    />

                    <input
                        type="reset"
                        value="Cancel"
                        className="cursor-pointer p-2 bg-red-600 hover:bg-red-700 active:bg-red-800 rounded-sm font-bold"
                    />
                </div>
            </form>
        </div>
    );
}
