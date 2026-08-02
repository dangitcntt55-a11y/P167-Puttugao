import { DiagnosisDetail } from "@/components/diagnosis/diagnosis-detail";

export default function DiagnosisPage({ params }: { params: { diagnosisId: string } }) {
  return <DiagnosisDetail diagnosisId={parseInt(params.diagnosisId)} />;
}
