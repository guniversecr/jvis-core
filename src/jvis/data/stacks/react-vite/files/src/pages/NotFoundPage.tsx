import { Link } from 'react-router-dom';

export function NotFoundPage() {
  return (
    <div>
      <h2>404 — Page Not Found</h2>
      <p>The page you are looking for does not exist.</p>
      <Link to="/">Go Home</Link>
    </div>
  );
}
