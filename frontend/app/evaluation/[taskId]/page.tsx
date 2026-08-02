import { EvaluationReport } from "@/components/evaluation/evaluation-report";

export default function EvaluationPage({ params }: { params: { taskId: string } }) {
  return <EvaluationReport taskId={parseInt(params.taskId)} />;
}
