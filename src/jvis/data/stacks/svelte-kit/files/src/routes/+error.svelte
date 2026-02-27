<script lang="ts">
  import { page } from '$app/stores';
</script>

<div>
  <h2>{$page.status} — {$page.error?.message || 'Page Not Found'}</h2>
  <p>The page you are looking for does not exist.</p>
  <a href="/">Go Home</a>
</div>
