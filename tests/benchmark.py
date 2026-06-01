def compare_models(audits):

    models = {}

    for a in audits:
        name = a[1]

        if name not in models:
            models[name] = []

        models[name].append(a[5])

    comparison = {}

    for model, scores in models.items():
        comparison[model] = sum(scores) / len(scores)

    return comparison