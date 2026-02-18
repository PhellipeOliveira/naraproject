import { Navigate } from "react-router-dom";
import { isAdminAuthenticated } from "../lib/adminSession";

type Props = {
  children: JSX.Element;
};

export function ProtectedAdminRoute({ children }: Props) {
  if (!isAdminAuthenticated()) {
    return <Navigate to="/admin/login" replace />;
  }
  return children;
}
