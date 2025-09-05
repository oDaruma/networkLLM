# STYLE_GUIDE.md — Conventions

## Single Source of Truth (Sanity Config)
- Declare only here: `RANDOM_STATE`, `DATA_PATH`, `TARGET_COL`, `stage_root` in `src/networkllm/config.py`.
- Do not redeclare elsewhere; import from `networkllm.config`.

## Preprocessor (Derive & Refresh)
- Compute only here: `feature_names`, `cat_cols`, `num_cols`, `preprocessor` in `src/networkllm/preprocess/preprocessor.py`.
- Persist feature order to `staging/manifests/feature_names.json` if needed.

## Naming (Imperial)
- Use: `X_train/y_train`, `X_val/y_val`, `X_test/y_test`; `feature_names`, `cat_cols`, `num_cols`; `baseline_model`, `bayes`.

## Banners
- Each module/function begins with a concise “What this does / Why” banner.

## Fail-fast
- Prefer explicit exceptions; avoid defensive guards unless necessary for determinism.
